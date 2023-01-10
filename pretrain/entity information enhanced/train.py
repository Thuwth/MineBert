import os
import argparse

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import AutoModel, AutoTokenizer, AutoConfig
from transformers.optimization import AdamW, get_linear_schedule_with_warmup
from transformers import WEIGHTS_NAME, CONFIG_NAME
from utils import collate_fn, set_seeds
from options import args_parser
from tqdm import tqdm
from torch.optim import Adam
import wandb

from data_process import *
from model import LanguageModel, MaskLM
from optim_schedule import ScheduledOptim

args = args_parser()
wandb.init(project="st-inhanced-CE")

def train(epoch):
    vocab_path = os.path.join(args.tokenizer_name, args.vocab_file)
    print("----Loading vocab: \n", vocab_path)

    print("----Loading config: \n", args.config_name)
    config = AutoConfig.from_pretrained(args.config_name)

    print("----Loading tokenizer: \n", args.tokenizer_name)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name)

    # Load the train dataset
    train_path = os.path.join(args.data_path, args.train_file)
    print("----Loading train dataset \n", train_path)
    train_data = read_data(train_path)
    all_input_labels = get_masked_input_and_labels(train_data, tokenizer)
    features = data_prep(all_input_labels, tokenizer, vocab_path)

    # Create train data loader
    print("----Creating Dataloader")
    train_data_loader = DataLoader(features, batch_size=args.train_batch_size,
                                    shuffle=True, collate_fn=collate_fn,
                                    drop_last=True)
    
    # set the device
    device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

    # load the pretrained model or load the retrained model
    if not os.listdir(args.save_path):
        print("----Loading pretrained bert model: \n", args.model_name_or_path)
        bert_model = AutoModel.from_pretrained(args.model_name_or_path)
        model = LanguageModel(config, bert_model).to(device)
    else:
        model_path = os.path.join(args.save_path, "pytorch_model.bin")
        print("----Loading trained bert model from checkpoint: \n", model_path)
        bert_model = AutoModel.from_pretrained(args.save_path)
        model = LanguageModel(config, bert_model).to(device)

    # Setting the Adam optimizer with hyper-param
    optimizer = Adam(model.parameters(), lr=args.learning_rate)
    optim_schedule = ScheduledOptim(optimizer, config.hidden_size, n_warmup_steps=args.warmup_steps)

    # Using MSE loss function for predicting the mask_token
    criterion = nn.MSELoss(reduce=True)
    print("Total parameters:", sum([p.nelement() for p in model.parameters()]))
    
    # Start training
    print("----Training Start")

    # Setting the tqdm progress bar
    str_code = "train" if args.train else "test"
    data_iter = tqdm(
        enumerate(train_data_loader),
        desc="EP_%s:%d" %(str_code, epoch),
        total = len(train_data_loader),
        bar_format="{l_bar}{r_bar}"
    )

    avg_loss = 0.0
    for step, batch in data_iter:
        losses = []
        for i in range(args.train_batch_size):
            model.train()
            input = {
                "input_ids": torch.tensor([batch[0][i]]).to(device),
                "attention_mask": torch.tensor([batch[1][i]]).to(device)
            }
            labels = batch[2][i]
            mask_indexes = batch[3][i]
            _, loss = model(input, mask_indexes, labels, device)
            loss.requires_grad_()
            losses.append(loss)

            # backward and optimization only in train
            if train:
                optim_schedule.zero_grad()
                loss.backward()
                optim_schedule.step_and_update_lr()
        mean_loss = torch.mean(torch.tensor(losses))
        avg_loss += mean_loss
        a_loss = avg_loss / (i+1)


        post_fix = {
            "epoch": epoch,
            "iteration": step,
            "avg_loss": a_loss,
            "loss": loss.item()
        }
        wandb.log({
            "loss": loss.item(),
        })

        if step % args.log_freq == 0:
            data_iter.write(str(post_fix))
        
    print("EP%d_%s, avg_loss=" %(epoch, str_code),
            a_loss / len(data_iter))

    # Setting the save path
    output_dir = args.save_path
    model_to_save = model.model if hasattr(model, 'model') else model
    output_model_file = os.path.join(output_dir, WEIGHTS_NAME)
    output_config_file = os.path.join(output_dir, CONFIG_NAME)

    # save model and config
    torch.save(model_to_save.state_dict(), output_model_file)
    model_to_save.config.to_json_file(output_config_file)
    tokenizer.save_vocabulary(output_dir)


if __name__ == "__main__":
    for epoch in range(args.num_train_epochs):
        train(epoch)
            

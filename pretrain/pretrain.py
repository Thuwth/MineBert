from datasets import load_dataset
from torch import nn
import os
from transformers import *
from tokenizers import *
import json
import wandb
import warnings
warnings.filterwarnings('ignore')
# os.environ['CUDA_VISIBLE_DEVICES'] = "4,5,6,7"
wandb.init(project="bert-cased")

my_dataset = load_dataset('text', data_files={'train':'/data_sas/wth/BERT/vocab/data.txt'})
dataset = my_dataset["train"]
d = dataset.train_test_split(test_size=0.1)

###########################
# train the mine bert-cased
###########################

# hyper parameters
files = ['/data_sas/wth/BERT/vocab/data.txt']
vocab_size = 40000
max_len = 512
# whether to truncate
truncate_longer_samples = True
model_path = "/data_sas/wth/BERT/vocab/bert_cased/tokenizer"
output_dir = "/data_sas/wth/BERT/vocab/bert_cased/output/1"

# load the cased tokenizer
tokenizer =  BertTokenizerFast.from_pretrained(model_path)

# tokenizer the dataset
def encode_with_truncation(examples):
  """Mapping function to tokenize the sentences passed with truncation"""
  return tokenizer(examples["text"], truncation=True, padding="longest",
                   max_length=max_len, return_special_tokens_mask=True)

def encode_without_truncation(examples):
  """Mapping function to tokenize the sentences passed without truncation"""
  return tokenizer(examples["text"], return_special_tokens_mask=True, padding='longest')

encode = encode_with_truncation if truncate_longer_samples else encode_without_truncation

train_dataset = d["train"].map(encode, batched=True)
test_dataset = d["test"].map(encode, batched=True)

if truncate_longer_samples:
    # remove other columns and set input_ids and attention_mask as PyTorch tensors
    train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])
    test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])
else:
    # remove other columns, and remain them as Python lists
    test_dataset.set_format(columns=["input_ids", "attention_mask", "special_tokens_mask"])
    train_dataset.set_format(columns=["input_ids", "attention_mask", "special_tokens_mask"])

# 如果text没有被tokenizer padding， 这个函数可以实现padding
def data_padding(example):
    res = {}
    pad_token_id = tokenizer.convert_tokens_to_ids('[PAD]')
    sep_token_id = tokenizer.convert_tokens_to_ids('[SEP]')
    pad_token_type_id = 0
    pad_attention_mask = 0
    pad_special_tokens_mask = 1 
    seq_len = len(example['input_ids'])
    if seq_len < max_len:
        pad_len = max_len - seq_len
        for _ in range(pad_len):
            res['input_ids'] = example['input_ids'].append(pad_token_id)
            res['token_type_ids'] = example['token_type_ids'].append(pad_token_type_id)
            res['attention_mask'] = example['attention_mask'].append(pad_attention_mask)
            res['special_tokens_mask'] = example['special_tokens_mask'].append(pad_special_tokens_mask)
    else:
        res['input_ids'] = example['input_ids'][:511].append()
        res['token_type_ids'] = example['token_type_ids'][:512]
        res['attention_mask'] = example['attention_mask'].append(pad_attention_mask)[:512]
        res['special_tokens_mask'] = example['special_tokens_mask'].append(pad_special_tokens_mask)[:511].append(sep_token_id)
    return res

# initialize the model with config
model_config = BertConfig(vocab_size=vocab_size, max_position_embeddings=max_len)
model = BertForMaskedLM(config=model_config)

# initialize the data collator, randomly masking 20% (default is 15%) of the tokens for the Masked Language Modeling (MLM) task
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True, 
    mlm_probability=0.2,
)

training_args = TrainingArguments(
    output_dir=output_dir,
    evaluation_strategy="steps",
    overwrite_output_dir=True,
    num_train_epochs=10,
    per_device_train_batch_size=18,
    gradient_accumulation_steps=8,
    per_device_eval_batch_size=18,
    logging_steps=1000,
    save_steps=1000,
    # load_best_model_at_end=True,
    # save_totle_limit=3,
)

# initialize the trainer and pass everything to it
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# train the model
trainer.train()
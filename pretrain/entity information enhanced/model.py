from __future__ import absolute_import, division, print_function

import json
import os
import token

from transformers import *
import torch
import torch.nn as nn
import torch.nn.functional as F

class MaskLM(nn.Module):
    def __init__(self, hidden, vocab_size):
        """
        :param hidden: output size of BERT model
        :param vocab_size: the number of classes, a n-class classification problem
        """
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(hidden, vocab_size),
            # nn.ReLU(),
            # nn.Linear(1000, 5000),
            # nn.ReLU(),
            # nn.Linear(5000, 10000),
            # nn.ReLU(),
            # nn.Linear(10000, 20000),
            # nn.ReLU(),
            # nn.Linear(20000, vocab_size),
            nn.LogSoftmax(dim=-1)
        )
        # self.l1 = nn.Linear(hidden, 1000)
        # self.l2 = nn.Linear(1000, 5000)
        # self.l3 = nn.Linear(5000, 10000)
        # self.l4 = nn.Linear(10000, 20000)
        # self.l5 = nn.Linear(20000, vocab_size)
        # self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = x.requires_grad_()
        output = self.model(x)
        return output

# class LanguageModel(nn.Module):
#     def __init__(self, config, model):
#         """
#         :param config: The pretrained config of model
#         :param model: Pretrained model
#         """
#         super().__init__()
#         self.config = config
#         self.model = model
#         self.hidden_size = self.config.hidden_size
#         self.vocab_size = self.config.vocab_size
#         self.mask_lm = MaskLM(self.hidden_size, self.vocab_size)
#         self.loss_fn = nn.MSELoss(reduce=True, size_average=False)

#     def forward(self, feature, index, label):
#         # batch_size * sequence_len * embedding_dim
#         sequence_output = self.model(**feature)[0]
#         token_mid_output = sequence_output[-1][index]
#         token_output = self.mask_lm(token_mid_output)
#         loss = self.loss_fn(token_output, label)
#         return token_output, loss

class LanguageModel(nn.Module):
    def __init__(self, config, model):
        """
        :param config: The pretrained config of model
        :param model: Pretrained model
        """
        super().__init__()
        self.config = config
        self.model = model
        self.hidden_size = self.config.hidden_size
        self.vocab_size = self.config.vocab_size
        self.mask_lm = MaskLM(self.hidden_size, self.vocab_size)
        # self.loss_fn = nn.MSELoss(reduce=True, size_average=True)
        self.criterion = nn.BCEWithLogitsLoss()


    def forward(self, feature, mask_index, labels, device):
        # batch_size * sequence_len * embedding_dim
        sequence_output = self.model(**feature)[0]
        ls = []
        tokens_output = []
        for i, index in enumerate(mask_index):
            token_mid_output = sequence_output[-1][index]
            token_output = self.mask_lm(token_mid_output)
            l = self.criterion(token_output, torch.squeeze(torch.tensor([labels[i]]), 0).float().to(device))
            ls.append(l)
            tokens_output.append(token_output)
        loss = torch.mean(torch.tensor(ls))
        return tokens_output, loss
    


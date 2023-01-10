import json
import os
import copy
import numpy as np
import torch
from transformers import *
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import warnings
warnings.filterwarnings('ignore')

def read_data(data_file, ):
    fr = open(data_file, "r", encoding="UTF-8")
    data = json.load(fr)
    return data

def get_indexes(data, gs_tag="B-GS", gs_middle_tag="I-GS", gt_tag="B-GT", gt_middle_tag="I-GT"):
    def get_index(lst, tag, middle_tag):
        indexes = []
        for i in range(len(lst)):
            if lst[i] == tag and lst[i+1]!=middle_tag:
                indexes.append([i])
            elif lst[i] == tag and lst[i+1]==middle_tag:
                t = []
                t.append(i)
                for j in range(i, len(lst)):
                    if lst[j] == middle_tag and lst[j-1] == tag:
                        if j-1 == i:
                            t.append(j)
                    elif lst[j] == middle_tag and lst[j-2] == tag:
                        if j-2 == i:
                            t.append(j)
                    elif lst[j] == middle_tag and lst[j-3] == tag:
                        if j-3 == i:
                            t.append(j)
                    elif lst[j] == middle_tag and lst[j-4] == tag:
                        if j-4 == i:
                            t.append(j)
                    elif lst[j] == middle_tag and lst[j-5] == tag:
                        if j-5 == i:
                            t.append(j)
                    elif lst[j] == middle_tag and lst[j-6] == tag:
                        if j-5 == i:
                            t.append(j)
                    elif lst[j] == middle_tag and lst[j-1] == middle_tag:
                        t.append(j)
                    else:
                        continue
                indexes.append(t)
            else:
                continue
        return indexes
    gs_entity_indexes, gt_entity_indexes = [], []
    for sample in data:
        ori_sent = sample['ori_sent']
        tgt_sent = sample['tgt_sent']
        tags = sample['tags']
        gs_indexes = get_index(tags, tag=gs_tag, middle_tag=gs_middle_tag)
        gt_indexes = get_index(tags, tag=gt_tag, middle_tag=gt_middle_tag)
        gs_entity_indexes.append(gs_indexes)
        gt_entity_indexes.append(gt_indexes)
    return gs_entity_indexes, gt_entity_indexes

def map_word_token(data, tokenizer, ):
    all_word_tag_pairs, all_token_tag_pairs, all_pos_pairs = [], [], []
    for sample in tqdm(data):
        ori_sent = sample['ori_sent']
        tgt_sent = sample['tgt_sent']
        tags = sample['tags']
        words = tgt_sent.split(' ')
        words_len = len(words)
        tags_len = len(tags)
        assert words_len == tags_len
        word_tag_pairs, token_tag_pairs, pos_pairs = {}, {}, {}
        word_pos, temp_pos, token_pos = 0, -1, 0
        for i in range(tags_len):
            word = words[i]
            tag = tags[i]
            word_tag_pairs[word] = tag
            tokens = tokenizer.tokenize(word)
            tokens_offset_pos = []
            for j in range(len(tokens)):
                token_tag_pairs[tokens[j]] = tag
                token_pos = temp_pos + (j+1)
                tokens_offset_pos.append(token_pos)
            temp_pos = token_pos
            pos_pairs[i] = tokens_offset_pos
        all_pos_pairs.append(pos_pairs)
        all_word_tag_pairs.append(word_tag_pairs)
        all_token_tag_pairs.append(token_tag_pairs)
    return all_pos_pairs, all_token_tag_pairs, all_word_tag_pairs


def get_masked_input_and_labels(data, tokenizer):
    cls_token = ['[CLS]']
    sep_token = ['[SEP]']
    all_input_labels = []
    gs_entity_indexes, gt_entity_indexes = get_indexes(data)
    all_pos_pairs, all_token_tag_pairs, all_word_tag_pairs = map_word_token(data, tokenizer)
    data_len = len(data)
    for i in range(data_len):
        sample = data[i]
        tgt_sent = sample["tgt_sent"]
        gs_indexes, gt_indexes = gs_entity_indexes[i], gs_entity_indexes[i]
        pos_pairs, token_tag_pairs, word_tag_pairs = all_pos_pairs[i], all_token_tag_pairs[i], all_word_tag_pairs[i]
        gs_tokenized_sent = tokenizer.tokenize(tgt_sent)
        gt_tokenized_sent = tokenizer.tokenize(tgt_sent)

        gs_token_indexes, gt_token_indexes = [], []
        for gs_index in gs_indexes:
            tokens_indexes = []
            for index in gs_index:
                token_index = pos_pairs[index]
                tokens_indexes.append(token_index)
            gs_token_indexes.append(tokens_indexes)

        for gt_index in gt_indexes:
            tokens_indexes = []
            for index in gt_index:
                token_index = pos_pairs[index]
                tokens_indexes.append(token_index)
            gt_token_indexes.append(tokens_indexes)
            
        for tokens_indexes in gs_token_indexes:
            indexes = [element for lis in tokens_indexes for element in lis]
            data_with_labels = {}
            labels = []
            for index in indexes:
                labels.append(gs_tokenized_sent[index])
                gs_tokenized_sent[index] = "[MASK]"
            data_with_labels["data"] = cls_token + gs_tokenized_sent + sep_token
            data_with_labels["label"] = labels
            data_with_labels["mask_index"] = [(index+1) for index in indexes]
            gs_tokenized_sent = tokenizer.tokenize(tgt_sent)
            all_input_labels.append(data_with_labels)

        for tokens_indexes in gt_token_indexes:
            indexes = [element for lis in tokens_indexes for element in lis]
            data_with_labels = {}
            labels = []
            for index in indexes:
                labels.append(gt_tokenized_sent[index])
                gt_tokenized_sent[index] = "[MASK]"
            data_with_labels["data"] = cls_token + gt_tokenized_sent + sep_token
            data_with_labels["label"] = labels
            data_with_labels["mask_index"] = [(index+1) for index in indexes]
            gt_tokenized_sent = tokenizer.tokenize(tgt_sent)
            all_input_labels.append(data_with_labels)
    return all_input_labels

# def get_onehot_labels(vocab_file, labels):
#     fr = open(vocab_file, "r", encoding="UTF-8")
#     data = fr.readlines()
#     vocab = []
#     onehot_labels = []
#     for token in data:
#         t = token.split('\n')[0]
#         vocab.append(t)
#     for label in labels:
#         index = vocab.index(label)
#         onehot_label = [0] * len(vocab)
#         onehot_label[index] = 1
#         onehot_labels.append(onehot_label)
#     return onehot_labels

# def data_preper(input_labels, tokenizer, vocab_file):
#     features = []
#     for sample in input_labels:
#         feature = {}
#         tokens = sample["data"]
#         label = sample["label"]
#         mask_index = sample["mask_index"]
#         onehot_labels = get_onehot_labels(vocab_file, label)
#         input_ids = tokenizer.convert_tokens_to_ids(tokens)
#         input_ids_len = len(input_ids)
#         token_type_ids = [0] * input_ids_len
#         attention_mask = [1] * input_ids_len
#         feature = {
#             "input_ids": input_ids,
#             "token_type_ids": token_type_ids,
#             "attention_mask": attention_mask,
#             "label": onehot_labels,
#             "masked_token": label,
#             "mask_index": mask_index,
#         }
#         features.append(feature)
#     return features

def get_labels(vocab_file, sample, max_seq_len=512):  
    fr = open(vocab_file, "r", encoding="UTF-8")
    lines = fr.readlines()
    vocab = []
    labels = []
    for line in lines:
        v = line.strip()
        vocab.append(v)
    mask_index = sample["mask_index"]
    mask_tokens = sample["label"]
    assert len(mask_index) == len(mask_tokens)
    label = [0] * max_seq_len
    for i in range(len(mask_index)):
        index = vocab.index(mask_tokens[i])
        label[mask_index[i]] = index
    return label
        
def data_prep(all_input_labels, tokenizer, vocab_file):    
    features = []
    for sample in all_input_labels:
        feature = {}
        data = sample["data"]
        mask_tokens = sample["label"]
        mask_index = sample["mask_index"]
        label = get_labels(vocab_file, sample)
        input_ids = tokenizer.convert_tokens_to_ids(data)
        input_ids_len = len(input_ids)
        token_type_ids = [0] * input_ids_len
        attention_mask = [1] * input_ids_len
        feature = {
            "input_ids": input_ids,
            "token_type_ids": token_type_ids,
            "attention_mask": attention_mask,
            "label": label,
            "mask_token": mask_tokens,
            "mask_index": mask_index,
        }
        features.append(feature)
    return features
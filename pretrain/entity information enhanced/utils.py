import torch
import numpy as np
import random

def set_seeds(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0 and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

def collate_fn(batch):
    max_len = max([len(f["input_ids"]) for f in batch])
    input_ids = [f["input_ids"] + [0] * (max_len - len(f["input_ids"])) for f in batch]
    attention_mask = [[1.0] * len(f["input_ids"]) + [0.0] * (max_len - len(f["input_ids"])) for f in batch]
    labels = [f["label"] for f in batch]
    # input_ids = torch.tensor([input_ids], dtype=torch.long)
    # attention_mask = torch.tensor([attention_mask], dtype=torch.float)
    mask_indexes = [f["mask_index"] for f in batch]
    output = (input_ids, attention_mask, labels, mask_indexes)
    return output    
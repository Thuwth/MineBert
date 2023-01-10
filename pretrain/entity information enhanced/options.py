import argparse

def args_parser():
    parser = argparse.ArgumentParser(description="Arguments for training")
    parser.add_argument(
        "--data_path", 
        default="/data_sas/wth/BERT/vocab/info-enhanced/data",
        type=str
    )

    parser.add_argument(
        "--transformer_type", 
        default="bert",
        type=str
    )
    
    parser.add_argument(
        "--model_name_or_path",
        default="/data_sas/wth/BERT/vocab/bert_cased/output/1/checkpoint-34000",
        type=str
    )

    parser.add_argument(
        "--train_file",
        default="train.json",
        type=str
    )
    parser.add_argument(
        "--dev_file",
        default="dev.json",
        type=str
    )
    parser.add_argument(
        "--vocab_file",
        default="vocab.txt",
        type=str
    )
    parser.add_argument(
        "--save_path",
        default="/data_sas/wth/BERT/vocab/info-enhanced/output",
        type=str
    )

    parser.add_argument(
        "--config_name",
        default="/data_sas/wth/BERT/vocab/bert_cased/tokenizer/config.json",
        type=str,
        help="Pretrained config name or path"
    )
    parser.add_argument(
        "--tokenizer_name",
        default="/data_sas/wth/BERT/vocab/bert_cased/tokenizer",
        type=str,
        help="Pretrained tokenizer name or path used in the process of training"
    )
    parser.add_argument(
        "--max_seq_len",
        default=512,
        type=int,
        help="The maximum total input sequence length after tokenization"
    )

    # arguments of the process of training
    parser.add_argument(
        "--train",
        default=True,
        type=bool,
        help="whether train or test"
    )

    parser.add_argument(
        "--train_batch_size",
        default=200,
        type=int,
        help="Batch size for training"
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        default=1,
        type=int,
        help="Number of updates steps to accumulate before preforming a backward pass"
    )
    parser.add_argument(
        "--vocab_size",
        default=40000,
        type=int, 
        help="The size of vocabulary and equals to the number of labels"
    )
    parser.add_argument(
        "--learning_rate",
        default=5e-4,
        type=float,
        help="The initial learning rate of Adam"
    )
    parser.add_argument(
        "--adam_epsilon", 
        default=1e-5, 
        type=float,
        help="Epsilon for Adam optimizer."
    )
    parser.add_argument(
        "--max_grad_norm", 
        default=1.0, 
        type=float,
        help="Max gradient norm."
    )
    parser.add_argument(
        "--warmup_steps", 
        default=10000, 
        type=int,
        help="Warmup steps for Adam."
    )
    parser.add_argument(
        "--num_train_epochs", 
        default=10, 
        type=int,
        help="Total number of training epochs to perform."
    )
    parser.add_argument(
        "--evaluation_steps", 
        default=1, 
        type=int,
        help="Number of training steps between evaluations."
    )
    parser.add_argument(
        "--seed", 
        type=int, 
        default=66,
        help="random seed for initialization"
    )

    parser.add_argument(
        "--log_freq",
        default=1,
        type=int,
        help="the frequence of logging loss"
    )

    args = parser.parse_args(args=[])
    return args
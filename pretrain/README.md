# pretrain MineBert model

Pretraining a Mineralogy Bert for information extraction and sentence classification. Our codes refers to the official code of [huggingface transformers](https://huggingface.co/). 

We train the model on the abstracts of 220000 mineralogical articles. First, we clean the data of 220000 mineralogical articles, and the data after cleaning is about 500M. During the training, we used four tesla v100 for about four days.


## How To Run
You can run the training code directly using the following command line:

```bash
bash run.sh
```

Or you can train your own model with a different corpus.

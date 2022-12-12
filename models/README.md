# MineBert Models

## Data Acquisition

We obtained 220k mineralogical literatures and used their abstracts as raw data for pretraining MineBert, because the information contained in the abstracts is relatively concise.

## Data Preprocession

After obtaining the data, it is necessary to preprocess the data. First, convert all formatted text to txt format. Because the mineralogical text contains many special symbols, it is necessary to remove the special symbols from the text. Finally, the whole mineralogical text is divided into sentences and stored in the txt text in the form of sentence by line.

## Pretraining

We use [huggingface transformers](https://huggingface.co/docs/transformers/index) as backbone in the pretraining process. When we trianing from scratch, we re-constrauct a vocal list which include 40000 tokens, it contains most of the special words of mineralogy. When we retrain the MineBert based on Bert, we re-use the original tokenizer from bert-base-cased and bert-bae-uncased to maintain the consistency of the segmentation results.

The pre-trained models of mineralogy are stored [here](https://cloud.tsinghua.edu.cn/d/c513b4b532c64d718695/). These models are pretrained on the corpus including mineralogy abstracts. You can download the pre-trained model and use MineBert as following:

```python
from transformers import *
minebert = AutoModel.from_pretrained("your_path_of_pretrained_model")
toknenizer = AutoTokenizerFast.from_pretrained("your_path_of_tokenizer")

sentence = "Limestone comes from the Himalayas."
inputs = tokenizer(sentence)
output = minebert(**input)
```

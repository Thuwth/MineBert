# MineBert Models

The pre-trained models of mineralogy are stored here.
We pretrained two types of models, which including training from Bert and training from scratch. 
The pre-trained models of mineralogy are stored [here](https://cloud.tsinghua.edu.cn/d/c513b4b532c64d718695/). These models are pretrained on the corpus including mineralogy abstracts. You can download the pre-trained model and use MineBert as following:

```python
from transformers import *
minebert = AutoModel.from_pretrained("your_path_of_pretrained_model")
toknenizer = AutoTokenizerFast.from_pretrained("your_path_of_tokenizer")

sentence = "Limestone comes from the Himalayas."
inputs = tokenizer(sentence)
output = minebert(**input)
```


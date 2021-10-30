# Japanese-LUW-Tokenizer

Japanese Long-Unit-Word (国語研長単位) Tokenizer for [Transformers](https://huggingface.co/transformers) based on [青空文庫](https://www.aozora.gr.jp/)

## Basic Usage

```py
>>> from transformers import RemBertTokenizerFast
>>> tokenizer=RemBertTokenizerFast.from_pretrained("Japanese-LUW-Tokenizer")
>>> tokenizer.tokenize("全学年にわたって小学校の国語の教科書に大量の挿し絵が用いられている")
['全', '学年', 'にわたって', '小学校', 'の', '国語', 'の', '教科書', 'に', '大量', 'の', '挿し', '絵', 'が', '用い', 'られ', 'ている']
```

## Installation

```sh
pip3 install 'transformers>=4.10.0' --user
git clone --depth=1 https://github.com/KoichiYasuoka/Japanese-LUW-Tokenizer
```


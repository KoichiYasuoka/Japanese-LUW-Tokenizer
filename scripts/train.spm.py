#! /usr/bin/python3 -i

import unicodedata
from tokenizers import SentencePieceUnigramTokenizer,trainers
from tokenizers.pre_tokenizers import Whitespace
from transformers import RemBertTokenizerFast,AutoTokenizer
tkz=AutoTokenizer.from_pretrained("KoichiYasuoka/bert-base-japanese-luw-upos")
alp=[c for c in tkz.convert_ids_to_tokens([i for i in range(len(tkz))]) if len(c)==1 and unicodedata.name(c).startswith("CJK")]
with open("cjk.txt","w",encoding="utf-8") as f:
  print("\n".join(alp),file=f)
tkz=SentencePieceUnigramTokenizer(replacement=" ",add_prefix_space=False)
tkz.pre_tokenizer=Whitespace()
tkz.normalizer.handle_chinese_chars=False
trn=trainers.UnigramTrainer(vocab_size=250300,special_tokens=["[CLS]","[UNK]","[PAD]","[MASK]","[SEP]","<special0>","<special1>","<special2>","<special3>","<special4>","<special5>","<special6>","<special7>","<special8>","<special9>"],unk_token="[UNK]")
tkz._tokenizer.train(files=["cjk.txt","udja.luw.txt","aozora.luw.txt"],trainer=trn)
tkz.save("tokenizer.json")
tokenizer=RemBertTokenizerFast(tokenizer_file="tokenizer.json",vocab_file="/dev/null",bos_token="[CLS]",cls_token="[CLS]",unk_token="[UNK]",pad_token="[PAD]",mask_token="[MASK]",sep_token="[SEP]",do_lower_case=False,keep_accents=True)
tokenizer.save_pretrained("Japanese-SPM-Tokenizer")

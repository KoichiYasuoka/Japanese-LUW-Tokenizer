#! /usr/bin/python3 -i

import unicodedata
from tokenizers import CharBPETokenizer
from transformers import RemBertTokenizerFast,AutoTokenizer
tkz=AutoTokenizer.from_pretrained("KoichiYasuoka/bert-base-japanese-luw-upos")
alp=[c for c in tkz.convert_ids_to_tokens([i for i in range(len(tkz))]) if len(c)==1 and unicodedata.name(c).startswith("CJK")]
tkz=CharBPETokenizer(lowercase=False,unk_token="[UNK]",suffix="")
tkz.normalizer.handle_chinese_chars=False
tkz.train(files=["udja.luw.txt","aozora.luw.txt"],vocab_size=250300,min_frequency=2,limit_alphabet=20000,initial_alphabet=alp,special_tokens=["[CLS]","[UNK]","[PAD]","[MASK]","[SEP]","<special0>","<special1>","<special2>","<special3>","<special4>","<special5>","<special6>","<special7>","<special8>","<special9>"],suffix="")
tkz.save("tokenizer.json")
tokenizer=RemBertTokenizerFast(tokenizer_file="tokenizer.json",vocab_file="/dev/null",bos_token="[CLS]",cls_token="[CLS]",unk_token="[UNK]",pad_token="[PAD]",mask_token="[MASK]",sep_token="[SEP]",do_lower_case=False,keep_accents=True)
tokenizer.save_pretrained("Japanese-LUW-Tokenizer")

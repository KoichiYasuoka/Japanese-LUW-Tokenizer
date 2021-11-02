#! /usr/bin/python3 -i

import unicodedata
from tokenizers import Tokenizer,models,pre_tokenizers,normalizers,decoders,trainers
from transformers import RemBertTokenizerFast,AutoTokenizer
tkz=AutoTokenizer.from_pretrained("KoichiYasuoka/bert-base-japanese-luw-upos")
alp=[c for c in tkz.convert_ids_to_tokens([i for i in range(len(tkz))]) if len(c)==1 and unicodedata.name(c).startswith("CJK UNIFIED")]
pst=tkz.backend_tokenizer.post_processor
tkz=Tokenizer(models.Unigram())
tkz.pre_tokenizer=pre_tokenizers.Whitespace()
tkz.normalizer=normalizers.Sequence([normalizers.Nmt(),normalizers.NFKC()])
trn=trainers.UnigramTrainer(vocab_size=250300,special_tokens=["[PAD]","[UNK]","[CLS]","[SEP]","[MASK]","<special0>","<special1>","<special2>","<special3>","<special4>","<special5>","<special6>","<special7>","<special8>","<special9>"],initial_alphabet=alp,unk_token="[UNK]",max_piece_length=16,n_sub_iterations=2)
tkz.train(files=["udja.luw.txt","aozora.luw.txt","aug.luw.txt"],trainer=trn)
tkz.post_processor=pst
tkz.decoder=decoders.WordPiece(prefix="",cleanup=True)
tkz.save("tokenizer.json")
tokenizer=RemBertTokenizerFast(tokenizer_file="tokenizer.json",vocab_file="/dev/null",bos_token="[CLS]",cls_token="[CLS]",unk_token="[UNK]",pad_token="[PAD]",mask_token="[MASK]",sep_token="[SEP]",do_lower_case=False,keep_accents=True)
tokenizer.save_pretrained("Japanese-LUW-Tokenizer")

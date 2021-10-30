#! /usr/bin/python3

from transformers import AutoModelForTokenClassification,AutoTokenizer,TokenClassificationPipeline
brt="KoichiYasuoka/bert-base-japanese-luw-upos"
mdl=AutoModelForTokenClassification.from_pretrained(brt)
tkz=AutoTokenizer.from_pretrained(brt,model_max_length=512)
nlp=TokenClassificationPipeline(model=mdl,tokenizer=tkz,aggregation_strategy="simple",device=0)
with open("aozora.txt","r",encoding="utf-8") as f, open("aozora.luw.txt","w",encoding="utf-8") as w:
  d=[]
  for r in f:
    if r.strip()!="":
      d.append(r.strip())
    if len(d)>255:
      for s in nlp(d):
        print(" ".join(t["word"] for t in s),file=w)
      d=[]
  if len(d)>0:
    for s in nlp(d):
      print(" ".join(t["word"] for t in s),file=w)

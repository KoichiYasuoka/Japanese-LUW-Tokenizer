#! /usr/bin/python3 -i

from transformers import AutoTokenizer,AutoConfig,AutoModelForTokenClassification,DataCollatorForTokenClassification,TrainingArguments,Trainer
from datasets.arrow_dataset import Dataset

brt="KoichiYasuoka/roberta-small-japanese-aozora"
tkz=AutoTokenizer.from_pretrained(brt)
with open("train.conllu","r",encoding="utf-8") as f:
  r=f.read()
tok,tag=[],[]
tk,tg=["[CLS]"],["SYM"]
for s in r.split("\n"):
  t=s.split("\t")
  if len(t)==10:
    w=tkz.tokenize(t[1])
    if len(w)==1:
      tk.append(w[0])
      tg.append(t[3])
    else:
      tk.append(w[0])
      tg.append("B-"+t[3])
      for c in w[1:]:
        tk.append(c)
        tg.append("I-"+t[3])
  elif len(tk)>63:
    if len(tk)<127:
      tk.append("[SEP]")
      tg.append("SYM")
      tok.append(list(tk))
      tag.append(list(tg))
      tk,tg=["[CLS]"],["SYM"]
    else:
      i=126
      while tg[i].startswith("I-"):
        i-=1
      tok.append(tk[0:i])
      tag.append(tg[0:i])
      tk,tg=tk[i:],tg[i:]
if len(tk)>1 and len(tk)<127:
  tk.append("[SEP]")
  tg.append("SYM")
  tok.append(list(tk))
  tag.append(list(tg))
lid={l:i for i,l in enumerate(set(sum(tag,[])))}
dts=Dataset.from_dict({"tokens":tok,"tags":tag,"input_ids":[tkz.convert_tokens_to_ids(s) for s in tok],"labels":[[lid[t] for t in s] for s in tag]})
cfg=AutoConfig.from_pretrained(brt,num_labels=len(lid),label2id=lid,id2label={i:l for l,i in lid.items()})
mdl=AutoModelForTokenClassification.from_pretrained(brt,config=cfg)
dcl=DataCollatorForTokenClassification(tokenizer=tkz)
arg=TrainingArguments(output_dir="/tmp",overwrite_output_dir=True,per_device_train_batch_size=4,save_total_limit=2)
trn=Trainer(model=mdl,args=arg,data_collator=dcl,train_dataset=dts)
trn.train()
b="roberta-small-japanese-luw-upos"
trn.save_model(b)
tkz.save_pretrained(b)

#! /usr/bin/python3 -i

import torch
from torch.utils.data.dataset import Dataset
from transformers import RemBertTokenizerFast,RobertaConfig,RobertaForMaskedLM,DataCollatorForLanguageModeling,TrainingArguments,Trainer

class LineByLineTextDataset(Dataset):
  def __init__(self,tokenizer,files,block_size):
    self.tokenizer=tokenizer
    self.block_size=block_size
    self.examples=[]
    for d in files:
      with open(d,"r",encoding="utf-8") as f:
        self.examples+=[s.strip() for s in f if s.strip()!=""]
  def __len__(self):
    return len(self.examples)
  def __getitem__(self,i):
    return {"input_ids":torch.tensor(self.tokenizer(self.examples[i],add_special_tokens=True,truncation=True,max_length=self.block_size)["input_ids"],dtype=torch.long)}

tokenizer=RemBertTokenizerFast.from_pretrained("/home/yasuoka/projects/Japanese-LUW-Tokenizer")
t=tokenizer.convert_tokens_to_ids(["[PAD]","[CLS]","[SEP]"])
config=RobertaConfig(pad_token_id=t[0],bos_token_id=t[1],eos_token_id=t[2],vocab_size=len(tokenizer),hidden_size=256,num_hidden_layers=12,num_attention_heads=4,intermediate_size=768,max_position_embeddings=128)
model=RobertaForMaskedLM(config)
dataset=LineByLineTextDataset(tokenizer=tokenizer,files=["udja.txt","aozora.txt","aug.txt"],block_size=126)
collator=DataCollatorForLanguageModeling(tokenizer=tokenizer,mlm=True,mlm_probability=0.15)
args=TrainingArguments(output_dir="/tmp",overwrite_output_dir=True,num_train_epochs=3,per_device_train_batch_size=8,warmup_steps=10000,learning_rate=2e-04,weight_decay=0.01,adam_beta1=0.9,adam_beta2=0.98,adam_epsilon=1e-04,save_steps=500,save_total_limit=2,seed=1)
trainer=Trainer(model=model,args=args,data_collator=collator,train_dataset=dataset)
trainer.train()
trainer.save_model("roberta-small-japanese-aozora")
tokenizer.save_pretrained("roberta-small-japanese-aozora")

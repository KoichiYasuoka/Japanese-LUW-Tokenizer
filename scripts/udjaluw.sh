#! /bin/sh
test -d UD_Japanese-GSD || git clone --depth=1 https://github.com/UniversalDependencies/UD_Japanese-GSD
test -d UD_Japanese-PUD || git clone --depth=1 https://github.com/UniversalDependencies/UD_Japanese-PUD
test -d UD_Japanese-Modern || git clone --depth=1 https://github.com/UniversalDependencies/UD_Japanese-Modern

python3 -c '
import glob
with open("udja.luw.txt","w",encoding="utf-8") as w, open("udja.txt","w",encoding="utf-8") as x:
  for d in glob.glob("UD_*/*.conllu"):
    with open(d,"r",encoding="utf-8") as f:
      r=f.read()
    tokens=[]
    for s in r.split("\n"):
      t=s.split("\t")
      if len(t)==10 and not s.startswith("#"):
        if t[0]=="1" or t[9].find("LUWBILabel=B")>=0:
          tokens.append(t[1])
        else:
          tokens[-1]=tokens[-1]+t[1]
      elif s.startswith("# text = "):
        print(s[9:],file=x)
      elif tokens!=[]:
        print(" ".join(tokens),file=w)
        tokens=[]
'
exit 0

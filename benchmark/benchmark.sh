#! /bin/sh

MODULE=${1-'esupar'}
LOAD=${2-'load("ja_luw")'}
CONLLU=${3-'maihime.conllu'}
TMP=/tmp/$MODULE.$$

python3 -c '
import '$MODULE'
nlp='"$MODULE.$LOAD"'
with open("'$CONLLU'","r",encoding="utf-8") as f:
  r=f.read()
import deplacy
with open("'$TMP'","w",encoding="utf-8") as f:
  for s in r.split("\n"):
    if s.startswith("# text = "):
      doc=nlp(s[9:])
      print(deplacy.to_conllu(doc),end="",file=f)
'
echo '###' $MODULE.$LOAD $CONLLU
python3 conll18_ud_eval.py $CONLLU $TMP
rm -f $TMP
exit 0

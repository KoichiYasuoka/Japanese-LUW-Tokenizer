#! /bin/sh
BERT=KoichiYasuoka/roberta-small-japanese-luw-upos
biaffine-dep train -b -d 0 -c biaffine-dep-en -p supar.model -f bert --bert $BERT --embed= --train train.conllu --dev UD_Japanese-GSDLUW/*-dev.conllu --test UD_Japanese-GSDLUW/*-test.conllu
cp -p supar.model $BERT/supar.model
exit 0

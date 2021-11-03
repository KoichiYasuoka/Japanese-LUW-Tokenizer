#! /bin/sh

exec biaffine-dep train -b -d 0 -c biaffine-dep-en -p supar.model -f bert --bert KoichiYasuoka/roberta-small-japanese-luw-upos --embed= --train train.conllu --dev UD_Japanese-GSDLUW/*-dev.conllu --test UD_Japanese-GSDLUW/*-test.conllu

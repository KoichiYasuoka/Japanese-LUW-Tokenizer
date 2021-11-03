#! /bin/sh
pip3 install 'transformers>=4.10.0' --user
./aozora.sh
python3 aozoraluw.py
./udjaluw.sh
python3 augment.py
python3 train.py
python3 roberta.py
ln -s . KoichiYasuoka
./conllu.sh
python3 uposroberta.py
pip3 install -U esupar --user
./esupar.sh

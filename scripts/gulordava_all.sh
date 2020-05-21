#!/bin/sh

# run from AgreementRNNs/

# Bock 1992 rc/pp
echo 'Bock1992'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/Bock1992/items.csv --scoring max,sample --paradigm prod

# Franck 2002 syntactic distance
echo 'Franck'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/Franck2002/items.csv --scoring max,sample --paradigm prod

# Bock 1999 pronouns vs subj verb
echo 'Bock199'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/Bock1999/items.csv --scoring max,sample --paradigm prod

# Haskell & MacDonald Conjunction linear distance
echo 'HaskellMacDonald'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/HaskellMacdonald2011/items.csv --scoring max,sample --paradigm prod

# Humphreys & Bock 2005 distributivity
echo 'HumphreysBock'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/HumphreysBock2005/items.csv --scoring max,sample --paradigm prod

# Parker & An 2018 argument status
echo 'ParkerAn'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/ParkerAn2018/items.csv --scoring max,sample --paradigm prod

python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/ParkerAn2018/items.csv --scoring surprisal --paradigm comp

# Wagers 2009 Agreement
echo 'Wagers2009'
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/Wagers2009/1_Baseline/items.csv --scoring surprisal --paradigm comp

# Wagers 2009 Illusion of Grammaticality
python eval_gulordava.py --model models/lstm-1,models/lstm-2,models/lstm-3,models/lstm-4,models/lstm-5 --data colorlessgreenRNNs/data/lm/English/ --input evalsets/Wagers2009/23_illusion/items.csv --scoring surprisal --paradigm comp

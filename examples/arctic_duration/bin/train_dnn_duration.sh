
python bin/train_duration.py
cat dur_feats/train/* > dur.train
cut -d ' ' -f 2- dur.train > dur_input.train
cut -d ' ' -f 1 dur.train > dur_output.train


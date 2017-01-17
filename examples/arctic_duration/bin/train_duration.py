import os

f = open('etc/txt.done.data.train')
for line in f:
    id  = line.split('\n')[0].split()[1]
    fname = 'dur_feats/' + id + '.dur'
    cmd = 'cp ' + fname + ' dur_feats/train'
    os.system(cmd)

f = open('etc/txt.done.data.test')
for line in f:
    id  = line.split('\n')[0].split()[1]
    fname = 'dur_feats/' + id + '.dur'
    cmd = 'cp ' + fname + ' dur_feats/test'
    os.system(cmd)


import os

vectors_file = 'vectors.txt'
phone_array = []
vector_array = []

f = open(vectors_file)

for line in f:
         
         line = line.split('\n')[0].split()
         #print line
         phone_array.append(line[0])
         vector_array.append(line[1:])

f = open('dur_input.test')
g = open('dur_input_test.vector','w')
for line in f:

           p_phone = line.split('\n')[0].split()[0]
           phone = line.split('\n')[0].split()[1]
           n_phone = line.split('\n')[0].split()[2]
           idx_p_phone = phone_array.index(p_phone)
           idx_phone = phone_array.index(phone)
           idx_n_phone = phone_array.index(n_phone)

           g.write(' '.join(i for i in (vector_array[idx_p_phone])))
           g.write( ' ' + ' '.join(i for i in (vector_array[idx_phone])))
           g.write(' ' + ' '.join(i for i in (vector_array[idx_n_phone])))
           g.write('\n')

g.close()
f.close()


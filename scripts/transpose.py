import numpy 
g = open('/home/srallaba/mgc/transposed/arctic_a0404.mgc','w')
x =  numpy.loadtxt('/home/srallaba/mgc_spaces/arctic_a0404.mgc')
numpy.savetxt(g, numpy.transpose(x))
g.close()  

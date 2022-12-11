#######################
#convertsinglefasta.py
#pass $proteinname, $run and $numcount+1

#for sys.argv
import sys

proteinname = sys.argv[1]
run = sys.argv[2]
count = eval(sys.argv[3])


#define paths
seq_dir = "../"+proteinname+"/output/"+run+"/seqs/"
out_dir = "../"+run+"/"
prefix = proteinname+"_"

#parameters
#count=100 #n

#read file
fastaname = proteinname+"_"+run+"_mpnn.fasta"
fa = open(fastaname,"w+")
for i in range(0,count): 
    fname = seq_dir+prefix+str(i)+".fa"
    fo = open(fname,"r")
    filenum = 0
    for line in fo:
        print(line)
        if ">" in line:
            print(line)
        else: 
            fa.writelines(">"+prefix+str(i)+"-"+str(filenum)+"\n")
            fa.writelines(line)
            filenum += 1
    fo.close()
else:
    fa.close()
    print("finished")

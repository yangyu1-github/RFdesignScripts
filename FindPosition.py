################################
# findposition.py
#pass $proteinname, $run and $numcount+1
#need to modify positions and sequence motifs for every design 

#for sys.argv
import sys

proteinname = sys.argv[1]
run = sys.argv[2]
count = eval(sys.argv[3])

fastaname = proteinname+"_"+run+".fasta"
positionfile = "mpnn.pos"
#count = 100 #n for .py n-1 for .ipynb
#define motif feature
motif1="MGHN"
motif2="CTF"
#define conserved positions, first position in a string is 0
pos1v1=1
pos1v2=2
pos1v3=3
pos1v4=4
pos2v1=1
pos2v2=2
pos2v3=3
pos2v4=6
pos2v5=10


fa = open(fastaname,"r")
fo = open(positionfile,"w+")
pos_1 = -1
pos_2 = -1

for i in range(0,count): 
    pos_ls = []
    newpos_ls = []
    seqname = fa.readline()
    #print(seqname)
    seq = fa.readline()
    pos_1 = seq.find(motif1)
    pos_2 = seq.find(motif2)
    pos_ls = [pos_1+pos1v1,pos_1+pos1v2,pos_1+pos1v3,pos_1+pos1v4,pos_2+pos2v1,pos_2+pos2v2,pos_2+pos2v3,pos_2+pos2v4,pos_2+pos2v5]
    pos_ls.sort()
    #print(pos_ls)
    newpos_ls = list(map(str,pos_ls))
    #print(newpos_ls)
    fo.writelines(" ".join(newpos_ls)+"\n")
    i += 1
fa.close()
fo.close()
print("findposition finished")


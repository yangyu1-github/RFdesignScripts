#pass $proteinname, $run and $numcount+1 and repeat_num

#for sys.argv
import sys

proteinname = sys.argv[1]
run = sys.argv[2]
protein_num = eval(sys.argv[3])
repeat_num = eval(sys.argv[4])

#define parameters
#protein_num = 100
#repeat_num = 3
#protein_name = "az"
folder = "../"+proteinname+"/output/"+run+"/OmegaFold_structure/"
plddt_file = run+"_plddt_ca.csv"

#initialize parameters
i = 0
j = 0

fa = open(plddt_file,"w+")
plddt = []

#calculate mean
def mean(numbers):
    s = 0.0
    for num in numbers:
        s = s + num
    return s / len(numbers)
    
#calculate

for i in range(protein_num):
    for j in range(repeat_num):
        ca_plddt = []
        ls = []
        pdb_name = folder+proteinname+"_"+str(i)+"-"+str(j)+".pdb"
        fo = open(pdb_name,"r")
        for line in fo:
            atom = line.split()
            if "CA" in atom:
                ca_plddt.append(float(atom[-2]))
        #plddt.append(mean(ca_plddt))
        ls = [proteinname+"_"+str(i)+"-"+str(j)+".pdb",str(mean(ca_plddt))]
        fa.write(",".join(ls)+"\n")
        fo.close()
        #print("repeat is "+str(j))
        j += 1 
    #print("protein number is "+str(i))
    i += 1
print(plddt) 
fa.close()

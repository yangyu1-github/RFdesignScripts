################################
# PDBtoFasta.py
#pass $proteinname, $run and $numcount+1

#for sys.argv
import sys
from Bio.PDB.PDBParser import PDBParser

proteinname = sys.argv[1]
run = sys.argv[2]
count = eval(sys.argv[3])

prefix=proteinname+"_"
pdb_dir="../"+proteinname+"/output/"+run+"/trf_relax/"
fastaname = proteinname+"_"+run+".fasta"
#count = 100 # 0- n

# You can use a dict to convert three letter code to one letter code
d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

fa = open(fastaname,"w+")

for i in range(0,count): 
    record = pdb_dir+prefix+str(i)+".pdb"
# run parser    
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('struct', record) 
# iterate each model, chain, and residue
    for model in structure:
        for chain in model:
            seq = []
            for residue in chain:
                seq.append(d3to1[residue.resname])
# printing out the sequence for each chain
#            fa.writelines('>'+prefix+str(i)+'\n',''.join(seq))
            fa.writelines('>'+prefix+str(i)+'\n')
            fa.writelines(seq)
            fa.writelines('\n')
else:
    fa.close()
    print("PDBtoFasta finished")

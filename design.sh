#######
#global parameters

run="run4"
input_pdb="az1.pdb"
proteinname="az"
numcount=99  #n-1 
repeat_num=2

###
#partial hallucination
designin="input/"$input_pdb
designout="output/"${run}"/"${proteinname}
designlog="output/"${run}"/"${proteinname}_${run}".log"

python ../../RFDesign/hallucination/hallucinate.py --pdb=$designin --out=$designout --contigs=A43-47,A112-121 --len=50-90 --use_template True --force_aa A44-47,A112-114,A117,A121 --exclude_aa C --steps=g600,m1000 --num=100 --start_num=0 --w_rog 0.5 --rog_thresh=12 --nthreads=20 --save_pdb=True --track_step 50 &>> $designlog


##################
#relax part
##################
# Performs relax on TRFold structures.
#
outpath="output/"$run
outdir=$outpath/trf_relax
file_name=${proteinname}"_"
mkdir -p $outdir
task_file=`basename $outpath`.fold.list
for PDB in $outpath/*.pdb; do
  f=`basename $PDB .pdb`
  NPZ=`dirname $PDB`/$f.npz
  if [ ! -f $outdir/$f.pdb ]; then
    echo "$DIR/RosettaTR/trfold_relax.py $roll -sg 7,3 $NPZ $PDB $outdir/$f.pdb"
  fi
done > $task_file

count=$(cat $task_file | wc -l)
printf "$count\n"
while (($count>=0))
do
    echo "Relaxing $count designs..."
    python ../../RFDesign/scripts/RosettaTR/trfold_relax.py -sg 7,3 ${outpath}/${file_name}${count}.npz ${outpath}/${file_name}${count}.pdb ${outdir}/${file_name}${count}.pdb
    ((count = count -1)) 


done


cd $outdir
ct=$(find ../ -maxdepth 1 -name '*.trb' | wc -l)
if [ "$ct" -gt 0 ]; then
    ln -sf ../*.trb .
fi

# change directory to the original one
cd /home/yang/Documents/Design/$proteinname

#
python ../../RFDesign/scripts/pyrosetta_metrics.py output/$run/trf_relax/


####################
#preparation of sequence and position file for ProteinMPNN
####################

python PDBtoFasta.py $proteinname $run $((numcount+1))

python FindPosition.py $proteinname $run $((numcount+1)) #need to modify for every design

##################
#mpnn part
##################

#define path
stored_pdbs="../"${proteinname}"/output/"${run}"/trf_relax/"
folder_with_pdbs="../"${proteinname}"/output/"${run}"/pdbs/"
prefix=${proteinname}"_"
output_dir="../"${proteinname}"/output/"${run}"/"

path_for_parsed_chains="parsed_pdbs.jsonl"
path_for_assigned_chains="assigned_pdbs.jsonl"
path_for_fixed_positions="fixed_pdbs.jsonl"

#define design parameters
chains_to_design="A"


#create directory
mkdir -p $folder_with_pdbs

#read positions from the list
readarray -t fixed_pos < mpnn.pos

#design loop
i=0

while ((i<=numcount))
do
	cp $stored_pdbs$prefix$i.pdb $folder_with_pdbs
	python ../../ProteinMPNN/helper_scripts/parse_multiple_chains.py --input_path=$folder_with_pdbs --output_path=$path_for_parsed_chains

	python ../../ProteinMPNN/helper_scripts/assign_fixed_chains.py --input_path=$path_for_parsed_chains --output_path=$path_for_assigned_chains --chain_list $chains_to_design

	python ../../ProteinMPNN/helper_scripts/make_fixed_positions_dict.py --input_path=$path_for_parsed_chains --output_path=$path_for_fixed_positions --chain_list $chains_to_design --position_list "${fixed_pos[i]}"

	python ../../ProteinMPNN/protein_mpnn_run.py \
        --jsonl_path $path_for_parsed_chains \
        --chain_id_jsonl $path_for_assigned_chains \
        --fixed_positions_jsonl $path_for_fixed_positions \
        --out_folder $output_dir \
        --num_seq_per_target $repeat_num \
        --sampling_temp "0.1" \
        --batch_size 1

	i=$((i+1))
	rm $folder_with_pdbs/*.pdb
done

fixed_pos={}

#fasta
python convertsinglefasta.py $proteinname $run $((numcount+1))

#OmegaFold
omegafold ${proteinname}_${run}_mpnn.fasta ../${proteinname}/output/${run}/OmegaFold_structure --num_cycle 4 

#calculate plddt
python plddt_calc.py $proteinname $run $((numcount+1)) $((repeat_num+1)) 

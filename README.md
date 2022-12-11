# RFdesignScripts
scripts to streamline RFdesign and MPNN
-prerequisite:
RFDesign,ProteinMPNN,OmegaFold,PyRosetta
-design flow:
RFDesign(hallucination or inpainting)-relax-evaluation using PyRosetta-determine position to keep in MPNN (PDBtoFasta.py, FindPosition.py)-ProteinMPNN-generate a single fasta file (convertsinglefasta.py)-Predict structure using OmegaFold-get plddt values (plddt_calc.py)

#!/bin/bash
#SBATCH --account=rrg-rmcintos
#SBATCH --mem=8000MB
#SBATCH --time=0-3:00


noise=${1} 
G=${2}
Jn=${3}
Ji=${4}
Wp=${5}

python single_sim_runner.py ${noise} ${G} ${Jn} ${Ji} ${Wp} 
matlab -nodisplay -nosplash -nodesktop -r "noise=${noise}; G=${G}; Jn=${Jn}; Ji=${Ji}; Wp=${Wp}; run('mse');exit;"


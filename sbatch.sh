#!/bin/bash
#SBATCH --account=rrg-rmcintos
#SBATCH --mem=8000MB
#SBATCH --time=0-6:36


noise=${1} 
G=${2}
Jn=${3}
Ji=${4}
Wp=${5}

python single_sim_runner.py ${noise} ${G} ${Jn} ${Ji} ${Wp} 

#!/bin/bash
#SBATCH --account=rrg-rmcintos
#SBATCH --mem=8000MB
#SBATCH --time=0-6:36


noise=${1} 
G=${2}
Mi=${3}
Jn=${4}
Ji=${5}
Wi=${6}
We=${7}

python single_sim_runner.py ${noise} ${G} ${Mi} ${Jn} ${Ji} ${Wi} ${We} 

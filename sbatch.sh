#!/bin/bash
#SBATCH --account=rrg-rmcintos
#SBATCH --mem=8000MB
#SBATCH --time=0-3:00
#SBATCH --array=1-100  # Example, replace 100 with the number of lines in your parameter file

# Read parameters from file
paramfile=$1
log_directory=$2
index=$SLURM_ARRAY_TASK_ID
read -r noise G Jn Ji Wp <<< $(sed -n "${index}p" $paramfile)

# Log file naming based on parameters
log_file="${log_directory}/params_sim_noise-${noise}_G-${G}_Jn-${Jn}_Ji-${Ji}_Wp-${Wp}.out"

# Running simulations
python single_sim_runner.py ${noise} ${G} ${Jn} ${Ji} ${Wp} > "$log_file"
matlab -nodisplay -nosplash -nodesktop -r "noise=${noise}; G=${G}; Jn=${Jn}; Ji=${Ji}; Wp=${Wp}; run('mse');exit;" >> "$log_file"

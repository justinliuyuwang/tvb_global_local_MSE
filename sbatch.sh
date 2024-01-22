#!/bin/bash
#SBATCH --account=rrg-rmcintos
#SBATCH --mem=8000MB
#SBATCH --time=0-3:00

paramfile=$1
log_directory=$2
num_simulations_per_job=$3
index=$SLURM_ARRAY_TASK_ID

# Calculate start and end line for this job
start_line=$(( (index - 1) * num_simulations_per_job + 1 ))
end_line=$(( index * num_simulations_per_job ))

# Ensure end line does not exceed the total number of lines
total_lines=$(wc -l < "$paramfile")
if [ $end_line -gt $total_lines ]; then
    end_line=$total_lines
fi

# Loop over the specified range of lines
for i in $(seq $start_line $end_line); do
    read -r noise G Jn Ji Wp <<< $(sed -n "${i}p" $paramfile)
    log_file="${log_directory}/sim_${i}_noise-${noise}_G-${G}_Jn-${Jn}_Ji-${Ji}_Wp-${Wp}.out"

    # Run simulations and Matlab calls
    python single_sim_runner.py ${noise} ${G} ${Jn} ${Ji} ${Wp} > "$log_file"
    matlab -nodisplay -nosplash -nodesktop -r "noise=${noise}; G=${G}; Jn=${Jn}; Ji=${Ji}; Wp=${Wp}; run('mse');exit;" >> "$log_file"
done

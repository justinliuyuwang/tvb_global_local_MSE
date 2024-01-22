#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 23 ]; then
    echo "Usage: $0 paramfile log_directory min_noise max_noise num_noise_values min_G max_G num_G_values min_Jn max_Jn num_Jn_values min_Ji max_Ji num_Ji_values min_Wp max_Wp num_Wp_values"
    echo "Example: $0 param.txt /path/to/log_dir 1e-5 2e-5 3 0.01 0.02 3 1.0 1.1 3 1 1 1 1.0 1.5 3 "
    exit 1
fi

paramfile=$1

log_directory=$2



min_noise=$3
max_noise=$4
num_noise_values=$5


min_G=$6
max_G=$7
num_G_values=$8

min_Jn=${9}
max_Jn=${10}
num_Jn_values=${11}

min_Ji=${12}
max_Ji=${13}
num_Ji_values=${14}

min_Wp=${15}
max_Wp=${16}
num_Wp_values=${17}


# my_G=0.01
# my_noise=1e-5

# Mi=1.0
# Jn=0.15
# Ji=1.0
# Wi=0.7
# We=1.0



# Function to generate equally spaced values between min and max, inclusive
generate_values() {
    local min=$1
    local max=$2
    local num_values=$3
    local increment
    increment=$(bc -l <<< "scale=10; ($max - $min) / ($num_values - 1)") # Calculate increment

    local values=()
    for ((i=0; i<num_values; i++)); do
        local value
        value=$(bc -l <<< "scale=10; $min + ($increment * $i)") # Calculate each value
        values+=($value)
    done
    echo "${values[@]}"
}

# Generate parameter values
noise_values=($(generate_values $min_noise $max_noise $num_noise_values))
G_values=($(generate_values $min_G $max_G $num_G_values))
Jn_values=($(generate_values $min_Jn $max_Jn $num_Jn_values))
Ji_values=($(generate_values $min_Ji $max_Ji $num_Ji_values))
Wp_values=($(generate_values $min_Wp $max_Wp $num_Wp_values))

# Create combinations and write them to the file
> "$paramfile"  # Clear the file before writing


# Varying Mi
for my_noise in "${noise_values[@]}"; do
    echo "$my_noise 0 0 0 0" >> "$paramfile"
done

# Varying Mi
for my_G in "${G_values[@]}"; do
    echo "0 $my_G 0 0 0" >> "$paramfile"
done

# Varying Mi
for Jn in "${Jn_values[@]}"; do
    echo "0 0 $Jn 0 0" >> "$paramfile"
done

# Varying Mi
for Ji in "${Ji_values[@]}"; do
    echo "0 0 0 $Ji 0" >> "$paramfile"
done

# Varying Mi
for Wp in "${Wp_values[@]}"; do
    echo "0 0 0 0 $Wp" >> "$paramfile"
done

# Calculate the number of lines in the parameter file
num_lines=$(wc -l < "$paramfile")

# Number of simulations each sbatch job should run
num_simulations_per_job=5

# Calculate the number of jobs needed
num_jobs=$(( (num_lines + num_simulations_per_job - 1) / num_simulations_per_job ))

# Submit job array
sbatch --array=1-${num_jobs} "sbatch.sh" "$paramfile" "$log_directory" "$num_simulations_per_job"

# Read subjects and parameter combinations, then submit batch jobs
#    while read -r my_noise my_G Jn Ji Wp; do
#        sbatch -J "params_sim_noise-${my_noise}_G-${my_G}_Jn-${Jn}_Ji-${Ji}_Wp-${Wp}" -o "${log_directory}/params_sim_noise-${my_noise}_G-${my_G}_Jn-${Jn}_Ji-${Ji}_Wp-${Wp}.out" "sbatch.sh" "${my_noise}" "${my_G}" "${Jn}" "${Ji}" "${Wp}"
#    done < "$paramfile"


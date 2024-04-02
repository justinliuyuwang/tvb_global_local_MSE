import numpy as np
import os
from scipy.io import loadmat, savemat
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
# Define the directory containing the .mat files and the log file
directory = '/home/jwangbay/scratch/nadeen/final/final/pse_img/'
log_file_path = '/home/jwangbay/scratch/nadeen/final/final/log/params.txt'

# Specify the noise value of interest and default values for other parameters
noise_value = '0.0005'
default_values = {'G': '2', 'Jn': '0.15', 'Ji': '1', 'Wp': '1.4'}

# Format specifier for constructing filenames
formatSpec = '%.6f'


def format_number(value):
    """
    Format a number using fixed-point or exponential notation, whichever is more
    compact, with up to 6 significant digits. This mimics MATLAB's %.6g behavior.
    
    Parameters:
    - value: The number to format.
    
    Returns:
    A string representation of the number formatted according to the rules of %.6g.
    """
    return f"{value:.6g}"


# Function to read parameters and their values from the log file
def read_params_from_log(log_file_path, active_param, noise_value, default_values):
    parameter_values = set()
    with open(log_file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 6:
                noise, G, Jn, Ji, Wp, noise_seed = values
                if noise == noise_value:
                    if all(values[i+1] == default_values[param] for i, param in enumerate(default_values) if param != active_param):
                        param_value = values[list(default_values.keys()).index(active_param) + 1]
                        parameter_values.add(param_value)
    return sorted(parameter_values)

def plot_entropy_values(active_param, all_vectors, all_params):
    # Combine the vectors and params for sorting
    combined = list(zip(all_vectors, all_params))
    # Sort by parameter value
    combined_sorted = sorted(combined, key=lambda x: x[1])
    # Unpack them back into sorted lists
    all_vectors_sorted, all_params_sorted = zip(*combined_sorted)
    
    # Now, all_vectors_sorted and all_params_sorted are sorted by the parameter value
    colors = np.linspace(0, 1, len(all_params_sorted))
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["blue", "red"])
    
    plt.figure(figsize=(10, 6))
    for i, vectors in enumerate(all_vectors_sorted):
        color = cmap(colors[i])
        # You might need to adjust the indexing based on how your entropy values are structured
        plt.plot(vectors.mean(axis=0), color=color, alpha=0.5, label=f'{format(active_param)}={all_params_sorted[i]:.4f}')
    
    plt.title(f'MSE for Varying {active_param}')
    plt.xlabel('Time Scale')
    plt.ylabel('Entropy Value')
    plt.tight_layout()
    plt.savefig(f"{active_param}_MSE_change.png", bbox_inches='tight')

    
# Function to load vectors using exact file matching
def load_vectors(directory, active_param, parameter_values, noise_seed):
    vectors = []
    for value in parameter_values:
        # filename = f"vectorized_entropy_values_noise-{noise_value}_G-{parameter_values[0]}_Jn-{parameter_values[1]}_Ji-{parameter_values[2]}_Wp-{parameter_values[3]}_noiseseed-{noise_seed}.mat"
        # filename = f"vectorized_entropy_values_noise-{formatSpec % float(noise_value)}_G-{formatSpec % float(default_values['G']) if active_param != 'G' else formatSpec % value}_Jn-{formatSpec % float(default_values['Jn'])}_Ji-{formatSpec % float(default_values['Ji'])}_Wp-{formatSpec % float(default_values['Wp'])}_noiseseed-{formatSpec % float(noise_seed)}.mat"
        # filename = f"vectorized_entropy_values_noise-{noise_value}_G-{default_values['G'] if active_param != 'G' else value}_Jn-{default_values['Jn'] if active_param != 'Jn' else value}_Ji-{default_values['Ji'] if active_param != 'Ji' else value}_Wp-{default_values['Wp'] if active_param != 'Wp' else value}_noiseseed-{noise_seed}.mat"
        my_G=default_values['G'] if active_param!='G' else str(format_number(float(value))) 
        my_Jn=default_values['Jn'] if active_param!='Jn' else str(format_number(float(value))) 
        my_Ji=default_values['Ji'] if active_param!='Ji' else str(format_number(float(value))) 
        my_Wp=default_values['Wp'] if active_param!='Wp' else str(format_number(float(value))) 
        filename = f"vectorized_entropy_values_noise-{noise_value}_G-{my_G}_Jn-{my_Jn}_Ji-{my_Ji}_Wp-{my_Wp}_noiseseed-{noise_seed}.mat"

        # print(filename)
        full_path = os.path.join(directory, filename)
        if os.path.exists(full_path):
            data = loadmat(full_path)
            # vectors.append(data['a_vector'].flatten())


            entropy_values = data['a_vector'][0]
            flattened_array = np.concatenate([item.flatten() for item in entropy_values])
            vectors.append(flattened_array)

    if vectors:
        # return np.vstack(vectors), np.array(parameter_values)

        return np.vstack(vectors), np.vstack(np.array(parameter_values)),vectors, parameter_values
    else:
        return np.empty((0,)), np.array([]),np.empty((0,)), np.array([])
        print("NO VECTORS")

# Read noise seeds from the log file to consider all combinations
def read_noise_seeds(log_file_path):
    noise_seeds = set()
    with open(log_file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 6:
                noise_seeds.add(values[-1])
    return noise_seeds

noise_seeds = [1,2,3,4,5,6,7,8] #read_noise_seeds(log_file_path)

all_vectors = {}
all_params = {}
all_vectors1 = []
all_params1 = []
for active_param in ['G', 'Jn', 'Ji', 'Wp']:
    all_vectors[active_param] = []
    all_params[active_param] = []
    
    for noise_seed in noise_seeds:
        parameter_values = read_params_from_log(log_file_path, active_param, noise_value, default_values)
        stacked_vectors, param_values,vectors, params = load_vectors(directory, active_param, parameter_values, noise_seed)
        if vectors:
            all_vectors1.extend(vectors)
            all_params1.extend(params)
        if stacked_vectors.size > 0:
            all_vectors[active_param].append(stacked_vectors)
            for i,item in enumerate(parameter_values):
                parameter_values[i]=float(item)
            all_params[active_param].extend(parameter_values)  # Assuming parameter_values is a list of values for each vector
        else:
            print(f"No vectors found for varying {active_param} with noise={noise_value}, noise_seed={noise_seed}, and default values for other parameters.")
    
    plot_entropy_values(active_param, all_vectors1, [float(param) for param in all_params1])
    
    # After processing all noise seeds, vertically stack the vectors and parameter values
    if all_vectors[active_param]:
        final_stacked_vectors = np.vstack(all_vectors[active_param])
        final_param_values = np.vstack(all_params[active_param])

        # Save the stacked vectors and parameter values as a .mat file
        output_filename = f'final_stacked_vectors_{active_param}.mat'
        if not os.path.exists(output_filename):
            savemat(output_filename, {'vectors': final_stacked_vectors, 'params': final_param_values})
            print(f"Saved {output_filename}.")
        else:
            print(f"{output_filename} exists ALREADY!")
    else:
        print(f"No vectors to save for {active_param}.")

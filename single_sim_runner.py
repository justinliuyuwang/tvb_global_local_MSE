import argparse
import model_wongwang
import showcase1_ageing as utils
import matplotlib.pyplot as plt
from scipy.io import savemat
import numpy as np

def format_float(f):
    return "{:.6g}".format(f)

def plot_ts_stack(data, x=None, scale=0.9, lw=0.4, c='k', title=None, labels=None, width=48, ax=None, alpha=1.0):
    data = data - np.mean(data, axis=0, keepdims=True)
    maxrange = np.max(np.max(data, axis=0) - np.min(data, axis=0))
    data /= maxrange
    if x is None:
        x = np.arange(data.shape[0])
    n_nodes = data.shape[1]
    if ax is None:
        fig, ax = plt.subplots(figsize=(width,0.5*n_nodes))
    for i in range(n_nodes):
        ax.plot(x, scale*data[:, i] + i, c, lw=lw, alpha=alpha)
        ax.autoscale(enable=True, axis='both', tight=True)
    if title is not None:
        ax.set_title(title)
    if labels is None:
        labels = np.r_[:n_nodes]
    ax.set_yticks(np.r_[:n_nodes])
    ax.set_yticklabels(labels)
    return ax


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Run the simulation model with specified parameters.")

    # Define arguments
    #parser.add_argument("subject", help="The subject parameter")
    parser.add_argument("noise", type=float, help="Noise level")
    parser.add_argument("G", type=float, help="Global coupling parameter")
    parser.add_argument("Jn", type=float, help="Excitatory mass parameter")
    parser.add_argument("Ji", type=float, help="Ji parameter")
    parser.add_argument("Wp", type=float, help="Wp parameter")
    parser.add_argument("noise_seed", type=float, help="noise seed parameter")
    

    # Parse arguments
    args = parser.parse_args()


    # Parameters based on parsed arguments
    parameters = [
        {"my_noise": args.noise,"my_G": args.G,"Jn": args.Jn, "Ji": args.Ji, "Wp": args.Wpm, "noise_seed": args.noise_seed}
    ]
    
    # Loop through each set of parameters
    for i, params in enumerate(parameters, start=1):
        # Run the model
        time, data = model_wongwang.process_sub(**params)

        formatted_noise = format_float(args.noise)
        formatted_G = format_float(args.G)
        formatted_Jn = format_float(args.Jn)
        formatted_Ji = format_float(args.Ji)
        formatted_Wp = format_float(args.Wp)
        formatted_noise_seed = format_float(args.noise_seed)

        # Plot and save time series stack
        #ax = plot_ts_stack(data[1*1000:20*1000:10, 0, :, 0], x=time[1*1000:20*1000:10]/1000., width=20)
        #ax.set(xlabel='time [s]')
        #plt.savefig(f"pse_img/ts_allroi_ww_run{i}_noise-{formatted_noise}_G-{formatted_G}_Jn-{formatted_Jn}_Ji-{formatted_Ji}_Wp-{formatted_Wp}.png")
        
        # Plot and save temporal average
        #plt.figure()
        #plt.plot(time, data[:, 0, :, 0], 'k', alpha=0.1)
        #plt.title("Temporal Average")
        #plt.savefig(f"pse_img/ts_allroi_regplot_ww_run{i}_noise-{formatted_noise}_G-{formatted_G}_Jn-{formatted_Jn}_Ji-{formatted_Ji}_Wp-{formatted_Wp}.png")
        
        # Save data for each ROI
        data = data[1000:]
        for roi in range(4):
            eeg = {'eeg': data[:, 0, roi, 0]}
            savemat(f'pse_img/eeg_roi{roi}_ww_run{i}_noise-{formatted_noise}_G-{formatted_G}_Jn-{formatted_Jn}_Ji-{formatted_Ji}_Wp-{formatted_Wp}_noiseseed-{formatted_noise_seed}.mat', eeg)
            eeg = {'eeg': data[:, 1, roi, 0]}
            savemat(f'pse_img/eeg_roi{roi}_ww_run{i}_noise-{formatted_noise}_G-{formatted_G}_Jn-{formatted_Jn}_Ji-{formatted_Ji}_Wp-{formatted_Wp}_noiseseed-{formatted_noise_seed}_v.mat', eeg)
if __name__ == "__main__":
    main()



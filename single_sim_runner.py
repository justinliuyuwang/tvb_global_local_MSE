import argparse
import model_wongwang
import showcase1_ageing as utils
import matplotlib.pyplot as plt
from scipy.io import savemat
import numpy as np



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

    # Parse arguments
    args = parser.parse_args()


    # Parameters based on parsed arguments
    parameters = [
        {"noise": args.noise,"G": 0,"Jn": 0, "Ji": 0, "Wp": 0},
        {"noise": 0,"G": args.G,"Jn": 0, "Ji": 0, "Wp": 0},
        {"noise": 0,"G": 0,"Jn": 0, "Ji": args.Ji, "Wp": 0},
        {"noise": 0,"G": 0,"Jn": args.Jn, "Ji": 0, "Wp": 0},
        {"noise": 0,"G": 0,"Jn": 0, "Ji": 0, "Wp": args.Wp}
    ]

    # Loop through each set of parameters
    for i, params in enumerate(parameters, start=1):
        # Run the model
        time, data = model_wongwang.process_sub(**params)

        # Plot and save time series stack
        ax = plot_ts_stack(data[1*1000:20*1000:10, 0, :, 0], x=time[1*1000:20*1000:10]/1000., width=20)
        ax.set(xlabel='time [s]')
        plt.savefig(f"pse_img/ts_allroi_ww_run{i}_noise-{args.noise}_G-{args.G}_Mi-{args.Mi}_Jn-{args.Jn}_Ji-{args.Ji}_Wi-{args.Wi}_We-{args.We}.png")

        # Plot and save temporal average
        plt.figure()
        plt.plot(time, data[:, 0, :, 0], 'k', alpha=0.1)
        plt.title("Temporal Average")
        plt.savefig(f"pse_img/ts_allroi_regplot_ww_run{i}_noise-{args.noise}_G-{args.G}_Mi-{args.Mi}_Jn-{args.Jn}_Ji-{args.Ji}_Wi-{args.Wi}_We-{args.We}.png")

        # Save data for each ROI
        data = data[1000:]
        for roi in range(76):
            eeg = {'eeg': data[:, 0, roi, 0]}
            savemat(f'pse_img/eeg_roi{roi}_ww_run{i}_noise-{args.noise}_G-{args.G}_Mi-{args.Mi}_Jn-{args.Jn}_Ji-{args.Ji}_Wi-{args.Wi}_We-{args.We}.mat', eeg)

if __name__ == "__main__":
    main()



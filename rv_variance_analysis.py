import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy.stats import pearsonr

# Step 1: Read the CSV file
df = pd.read_csv('timeseries_variability_backup.csv')

# Step 2: Define a function to create and save a heatmap
def create_heatmap(df, x, y, value, title, file_name):
    pivot_table = df.pivot_table(index=y, columns=x, values=value, aggfunc=np.mean)
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, cmap="viridis")  # Removed annot=True
    plt.title(title)
    plt.savefig(file_name)
    plt.close()

# Function to create heatmaps for each ROI's r and v variances
def create_roi_heatmaps(df, x, y, rois, noiseseed=None):
    for roi in rois:
        for var_type in ['r_var', 'v_var']:
            value_col = f'{roi}_{var_type}'
            if noiseseed is not None:
                # For individual noiseseeds
                title = f'Heatmap for {roi.upper()} {var_type} (Noise Seed: {noiseseed}, {x} vs. {y})'
                file_name = f'img/heatmap_{roi}_{var_type}_seed_{noiseseed}_{x}_vs_{y}.png'
            else:
                # For averaged across all noiseseeds
                title = f'Average Heatmap for {roi.upper()} {var_type} ({x} vs. {y})'
                file_name = f'img/heatmap_{roi}_{var_type}_average_{x}_vs_{y}.png'
            create_heatmap(df, x, y, value_col, title, file_name)


# Ensure the directory exists
os.makedirs('img', exist_ok=True)


# Extract unique values for noise_seed
noiseseeds = df['noise_seed'].unique()

# Define ROIs based on your CSV structure
rois = ['ROI_0', 'ROI_1', 'ROI_2', 'ROI_3']


# Step 4: Adjusted to print correlation and p-value, and create/save heatmaps
def print_correlation(df, parameter, rois):
    for roi in rois:
        for var_type in ['r_var', 'v_var']:
            value_col = f'{roi}_{var_type}'
            correlation, p_value = pearsonr(df[parameter], df[value_col])
            print(f'Comparing {parameter} with {value_col}: Correlation = {correlation:.3f}, p-value = {p_value:.3g}')

for parameter in ['G', 'Jn', 'Ji', 'Wp']:
    print(f'\nCorrelation and p-value for parameter: {parameter}')
    print_correlation(df, parameter, rois)
    create_roi_heatmaps(df, 'noise', parameter, rois)

# Step 3: Adjusted to create and save heatmaps for each noiseseed and each ROI's r and v variances
for seed in noiseseeds:
    df_seed = df[df['noise_seed'] == seed]
    for parameter in ['G', 'Jn', 'Ji', 'Wp']:
        create_roi_heatmaps(df_seed, 'noise', parameter, rois, noiseseed=seed)

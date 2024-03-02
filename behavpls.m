% Array of file paths
filePaths = {
    '/home/jwangbay/scratch/nadeen/final/final/final_stacked_vectors_G.mat',
    '/home/jwangbay/scratch/nadeen/final/final/final_stacked_vectors_Jn.mat',
    '/home/jwangbay/scratch/nadeen/final/final/final_stacked_vectors_Ji.mat',
    '/home/jwangbay/scratch/nadeen/final/final/final_stacked_vectors_Wp.mat'
};

% Array of number of subjects corresponding to each file
numSubjLsts = [808, 800, 800, 808];

% Titles for the figures
figureTitles = {
    'ALL subs Correlations for G LV ',
    'ALL subs Correlations for Jn LV ',
    'ALL subs Correlations for Ji LV ',
    'ALL subs Correlations for Wp LV '
};

% Titles for the figures
heatmapTitles = {
    'BSR for MSE for G',
    'BSR for MSE for Jn',
    'BSR for MSE for Ji',
    'BSR for MSE for Wp'
};

% Paths for saving correlation figures
correlationFigPaths = {
    '/home/jwangbay/scratch/nadeen/final/final/pls_behavpls_G_r_bsr_mse_lv',
    '/home/jwangbay/scratch/nadeen/final/final/pls_behavpls_Jn_r_bsr_mse_lv',
    '/home/jwangbay/scratch/nadeen/final/final/pls_behavpls_Ji_r_bsr_mse_lv',
    '/home/jwangbay/scratch/nadeen/final/final/pls_behavpls_Wp_r_bsr_mse_lv'
};

% Paths for saving BSR heatmap figures
heatmapFigPaths = {
    '/home/jwangbay/scratch/nadeen/final/final/reshaped_bsr_heatmap_plsG_mse_r.png',
    '/home/jwangbay/scratch/nadeen/final/final/reshaped_bsr_heatmap_plsJn_mse_r.png',
    '/home/jwangbay/scratch/nadeen/final/final/reshaped_bsr_heatmap_plsJi_mse_r.png',
    '/home/jwangbay/scratch/nadeen/final/final/reshaped_bsr_heatmap_plsWp_mse_r.png'
};

% Assuming lvs is defined elsewhere in your script
lvs = [1];

% Loop through each file
for idx = 1:numel(filePaths)
    % Load the data
    loadedData = load(filePaths{idx});
    all_subj = loadedData.vectors;
    all_age = (loadedData.params).';

    % Preprocess data
    all_subj(isnan(all_age), :) = [];
    all_age(isnan(all_age)) = [];

    datamat_lst{1} = all_subj;
    num_subj_lst = [numSubjLsts(idx)];
    num_cond = 1;

    % Setup and Run PLS
    option.method = 3;
    option.num_perm = 1000;
    option.num_split = 0;
    option.num_boot = 1000;
    option.stacked_behavdata = all_age.';

    res = pls_analysis(datamat_lst, num_subj_lst, num_cond, option);

	res.s
	res.perm_result.sprob % checking pvalues of the perm result

	res.boot_result.orig_corr(:,1)

    for lv_num = 1:length(lvs)
        lv = lvs(lv_num);

        % Generate and save correlation figure
        figure;
        tmp = res.boot_result.orig_corr(:, lv);
        bar(tmp, 'FaceColor', [0.75, 0.75, 0.75]); hold on;
        errorbar(1:length(tmp), tmp, tmp - res.boot_result.llcorr(:, lv), res.boot_result.ulcorr(:, lv) - tmp, 'LineWidth', 2);
        title(sprintf('%s%d', figureTitles{idx}, lv));
        hold off;
        saveas(gcf, sprintf('%s%d.png', correlationFigPaths{idx}, lv));

        % Generate and save BSR heatmap figure
        % Here's a direct approach to reshaping and plotting the heatmap
        % This part assumes 'res.boot_result.compare_u' is correctly shaped for plotting
bsr = res.boot_result.compare_u(:,lv);




% Assuming 'bsr' contains your flattened BSR data
totalDataPoints = numel(bsr); % Total number of BSR data points

% Calculate the number of columns, rounding up to ensure all data fits
numRows = 4;
numColumns = ceil(totalDataPoints / numRows);

% Reshape the data into 218 rows, padding with NaN if necessary
reshapedData = NaN(numRows, numColumns); % Initialize with NaN for padding
reshapedData(1:totalDataPoints) = bsr; % Fill in the BSR data

% Create the heatmap
figure;
h = heatmap(reshapedData);
        % Customizing the heatmap
        h.Colormap = jet;
        h.Title = sprintf('%s', heatmapTitles{idx});
        h.XLabel = 'Timescale';
        h.YLabel = 'ROI';
        h.XDisplayLabels = string(1:numColumns); % Timescale labels from 1 to 40
        h.YDisplayLabels = string(1:numRows); % ROI labels from 1 to 4

        saveas(gcf, heatmapFigPaths{idx});
    end
end




% G
% ans =

%   single

%     1.1376


% ans =

%      0


% ans =

%   single

%     0.3639




% Jn
% ans =

%   single

%     3.6805


% ans =

%      0


% ans =

%   single

%     0.4765





% Ji
% ans =

%   single

%     6.5853


% ans =

%      0


% ans =

%   single

%     0.6833


% Wp
% ans =

%   single

%     5.1571


% ans =

%      0


% ans =

%   single

%     0.8397

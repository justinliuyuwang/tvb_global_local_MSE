% Loop through each ROI
for roi = 0:75
    % Dynamically create the file path for each ROI
    file_path = strcat('pse_img/eeg_roi', int2str(roi), '_ww_run1.mat');
    %eeg_roi41_ww_run1.mat
    % Load the data from the file
    load(file_path);
    middle_rows = eeg;
    middle_rows = middle_rows';

    % Rest of your processing code...
    total_elements = numel(middle_rows);
    num_columns = floor(total_elements / 2000);
    truncated_elements = 2000 * num_columns;
    truncated_middle_rows = middle_rows(1:truncated_elements, :);
    reshaped_middle_rows = reshape(truncated_middle_rows, [2000, num_columns]);

    % Assuming get_mse_curve_across_trials_matlab is a function you have
    [a, b, c] = get_mse_curve_across_trials_matlab(reshaped_middle_rows);
    plot(c, a, "o");
    title_str = strcat('Mean MSE Curve for WW ROI ', int2str(roi));
    title(title_str);

    % Save the figure for each ROI
    saveas(gcf, strcat('pse_img/mean_mse_plot_ww_roi', int2str(roi), '.png'));
    clf;
end

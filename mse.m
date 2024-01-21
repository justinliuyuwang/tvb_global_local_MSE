disp(['Noise: ', num2str(noise)]);
disp(['G: ', num2str(G)]);
disp(['Jn: ', num2str(Jn)]);
disp(['Ji: ', num2str(Ji)]);
disp(['Wp: ', num2str(Wp)]);

% Loop through each ROI
for roi = 0:3
    % Dynamically create the file path for each ROI
    file_path = sprintf('pse_img/eeg_roi%d_ww_run1_noise%.2f_G%.2f_Jn%.2f_Ji%.2f_Wp%.2f.mat', roi, noise, G, Jn, Ji, Wp);
    
    % Load the data from the file
    if exist(file_path, 'file')
        load(file_path);
    else
        disp(['File not found: ', file_path]);
        continue; % Skip to the next iteration if file not found
    end
    
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
    title_str = sprintf('Mean MSE Curve for WW ROI %d', roi);
    title(title_str);

    % Save the figure for each ROI
    saveas(gcf, sprintf('pse_img/mean_mse_plot_ww_roi%d_noise%.2f_G%.2f_Jn%.2f_Ji%.2f_Wp%.2f.png', roi, noise, G, Jn, Ji, Wp));
    clf;
end

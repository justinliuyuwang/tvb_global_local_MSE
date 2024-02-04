formatSpec = '%.6g';

% Display parameters
disp(['Noise: ', num2str(noise, formatSpec)]);
disp(['G: ', num2str(G, formatSpec)]);
disp(['Jn: ', num2str(Jn, formatSpec)]);
disp(['Ji: ', num2str(Ji, formatSpec)]);
disp(['Wp: ', num2str(Wp, formatSpec)]);

% Define colors for each ROI
colors = ['r', 'g', 'b', 'k']; % Red, Green, Blue, Black

% Prepare to store data for each ROI
a_values = cell(1, 4);
c_values = cell(1, 4);
plotHandles = zeros(1, 4); % Array to store plot handles for legend

% Loop through each ROI
for roi = 0:3

    % Dynamically create the file path for each ROI
    file_path = sprintf(['pse_img/eeg_roi%d_ww_run1_noise-', formatSpec, '_G-', formatSpec, '_Jn-', formatSpec, '_Ji-', formatSpec, '_Wp-', formatSpec, '.mat'], roi, noise, G, Jn, Ji, Wp);
    
    % Load the data from the file
    if exist(file_path, 'file')
        load(file_path);
        delete(file_path); % Delete the .mat file after loading to save space
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
    
    % Store the data for plotting later
    [a, b, c] = get_mse_curve_across_trials_matlab(reshaped_middle_rows);
    a_values{roi+1} = a;
    c_values{roi+1} = c;
end

% Create a figure for the overlaid plots
figure;
hold on; % Hold on to plot multiple data sets in the same figure
for roi = 0:3
    % Plot points and store handle for legend
    plotHandles(roi+1) = plot(c_values{roi+1}, a_values{roi+1}, 'o', 'Color', colors(roi+1));
end
hold off;

% Add a legend and title
legend(plotHandles, {'ROI 0', 'ROI 1', 'ROI 2', 'ROI 3'}, 'Location', 'best');
title('Mean MSE Curves for WW ROIs');

% Save the overlayed plot figure
filename = sprintf(['pse_img/mean_mse_plots_overlay_ww_noise-', formatSpec, '_G-', formatSpec, '_Jn-', formatSpec, '_Ji-', formatSpec, '_Wp-', formatSpec, '.png'], noise, G, Jn, Ji, Wp);
saveas(gcf, filename);
clf;

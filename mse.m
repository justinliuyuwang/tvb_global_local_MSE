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

% Create a figure for the overlaid plots
figure;
hold on; % Hold on to plot multiple data sets in the same figure

% Loop through each ROI
for roi = 0:3

    % Dynamically create the file path for each ROI
    file_path = sprintf(['pse_img/eeg_roi%d_ww_run1_noise-', formatSpec, '_G-', formatSpec, '_Jn-', formatSpec, '_Ji-', formatSpec, '_Wp-', formatSpec, '.mat'], roi, noise, G, Jn, Ji, Wp);
    
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
    
    % Store the data for plotting later
    [a, b, c] = get_mse_curve_across_trials_matlab(reshaped_middle_rows);
    a_values{roi+1} = a;
    c_values{roi+1} = c;

    % Check for non-positive values for logarithmic fit
    positiveIndices = c_values{roi+1} > 0;
    xLog = log(c_values{roi+1}(positiveIndices));
    yLog = a_values{roi+1}(positiveIndices);

    % Fit a quadratic curve
    pQuad = polyfit(c_values{roi+1}, a_values{roi+1}, 2);
    xFitQuad = linspace(min(c_values{roi+1}), max(c_values{roi+1}), 100);
    yFitQuad = polyval(pQuad, xFitQuad);
    SSresidQuad = sum((a_values{roi+1} - polyval(pQuad, c_values{roi+1})).^2);
    SStotalQuad = (length(a_values{roi+1}) - 1) * var(a_values{roi+1});
    rsqQuad = 1 - SSresidQuad/SStotalQuad;

    % Fit a logarithmic curve
    pLog = polyfit(xLog, yLog, 1);
    yFitLog = polyval(pLog, xLog);
    SSresidLog = sum((yLog - polyval(pLog, xLog)).^2);
    SStotalLog = (length(yLog) - 1) * var(yLog);
    rsqLog = 1 - SSresidLog/SStotalLog;

    % Choose the best model and plot it
    if rsqQuad >= rsqLog
        plot(xFitQuad, yFitQuad, 'Color', colors(roi+1), 'LineWidth', 2);
    else
        plot(exp(xLog), yFitLog, 'Color', colors(roi+1), 'LineWidth', 2);
    end

    % Plot the data points for the current ROI
    plot(c_values{roi+1}, a_values{roi+1}, 'o', 'Color', colors(roi+1));
end

hold off;

% Add a legend and title
legend({'ROI 0', 'ROI 1', 'ROI 2', 'ROI 3'}, 'Location', 'best');
title('Best Fit Lines for WW ROIs');

% Save the overlayed plot figure
filename = sprintf(['pse_img/best_fit_plots_overlay_ww_noise-', formatSpec, '_G-', formatSpec, '_Jn-', formatSpec, '_Ji-', formatSpec, '_Wp-', formatSpec, '.png'], noise, G, Jn, Ji, Wp);
saveas(gcf, filename);
clf;

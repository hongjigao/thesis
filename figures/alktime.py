import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Replace with your actual file path
file_path = 'qee.xlsb.xlsx'  # Replace with your file path
sheet_name = 'alkjob'  # Replace with the name of your sheet
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract the columns
nbf = df['nbf']
memory = df['time']

# Apply logarithmic transformation to both axes (base 10) for fitting
log_nbf = np.log10(nbf)
log_memory = np.log10(memory)

# Split the data into two sets (for the fitting on log-transformed data)
# First set: points 1-4 (index 0 to 3)
log_nbf_1 = log_nbf[:4]
log_memory_1 = log_memory[:4]

# Second set: points 4-9 (index 3 to end)
log_nbf_2 = log_nbf[3:]
log_memory_2 = log_memory[3:]

# Perform linear regression on the first subset (points 1-4) on log-transformed data
slope_1, intercept_1, r_value_1, _, _ = stats.linregress(log_nbf_1, log_memory_1)

# Perform linear regression on the second subset (points 4-9) on log-transformed data
slope_2, intercept_2, r_value_2, _, _ = stats.linregress(log_nbf_2, log_memory_2)

# Generate fitted values for both subsets
# Since we fit the data on the log-transformed scale, we have to exponentiate back for the original scale
line_1 = 10 ** (slope_1 * log_nbf_1 + intercept_1)  # Convert back to original scale
line_2 = 10 ** (slope_2 * log_nbf_2 + intercept_2)  # Convert back to original scale

# Create the plot
plt.figure(figsize=(10, 8))  # Increased figure size for better readability

# Scatter plot of all original points
plt.scatter(nbf, memory, label='Data Points', color='blue', s=100)  # Increased marker size

# Plot the first linear fit for points 1-4 on the original data scale
plt.plot(nbf[:4], line_1, label=f'Fit 1: log(y) = {slope_1:.2f}·log(x) + {intercept_1:.2f}', color='red', linewidth=3)

# Plot the second linear fit for points 4-9 on the original data scale
plt.plot(nbf[3:], line_2, label=f'Fit 2: log(y) = {slope_2:.2f}·log(x) + {intercept_2:.2f}', color='green', linewidth=3)

# Set logarithmic scale for both x and y axes
plt.xscale('log')
plt.yscale('log')

# Add custom ticks for x and y axes with increased font size
plt.xticks([400, 600, 800, 1000, 1200, 1600],
           ['400', '600', '800', '1000', '1200', '1600'],
           fontsize=18)
plt.yticks([10000, 30000, 90000, 150000],
           ['10,000', '30,000', '90,000', '150,000'],
           fontsize=18)

# Increase the size of axis labels and title
plt.xlabel('Number of Basis Functions (nbf)', fontsize=22)
plt.ylabel('Time (seconds)', fontsize=22)
plt.title('Log-Log Plot of Time vs Nbf for Alkane Chain', fontsize=24, pad=20)

# Increase the size of equation and R^2 values
# Position the text inside the plot using relative coordinates
equation_text_1 = f"$\\log(y) = {slope_1:.2f}\\,\\log(x) + {intercept_1:.2f}$\n$R^2 = {r_value_1**2:.4f}$"
equation_text_2 = f"$\\log(y) = {slope_2:.2f}\\,\\log(x) + {intercept_2:.2f}$\n$R^2 = {r_value_2**2:.4f}$"

plt.text(0.05, 0.95, equation_text_1, transform=plt.gca().transAxes,
         fontsize=18, color='red', verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
plt.text(0.05, 0.75, equation_text_2, transform=plt.gca().transAxes,
         fontsize=18, color='green', verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

# Increase the size of legend text
plt.legend(fontsize=18)

# Adjust tick label sizes
plt.tick_params(axis='both', which='major', labelsize=18)

# Show grid (optional)

# Save and show the plot
plt.tight_layout()
plt.savefig('alktime.eps', format='eps')
plt.show()

import pandas as pd
import numpy as np

# Load the CSV file
file_path = "D:\\WiSee\\data\\finalDataset.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Function to generate synthetic data
def generate_synthetic_data(df, human_status, num_samples):
    # Filter data for the given human status
    filtered_data = df[df["Human Status"] == human_status]
    
    # Calculate mean and standard deviation for each receiver
    stats = filtered_data[["Receiver 1", "Receiver 2", "Receiver 3"]].agg(["mean", "std"])
    
    # Generate synthetic data
    synthetic_data = []
    for _ in range(num_samples):
        r1 = np.random.normal(stats.loc["mean", "Receiver 1"], stats.loc["std", "Receiver 1"])
        r2 = np.random.normal(stats.loc["mean", "Receiver 2"], stats.loc["std", "Receiver 2"])
        r3 = np.random.normal(stats.loc["mean", "Receiver 3"], stats.loc["std", "Receiver 3"])
        
        # Round RSSI values to whole numbers and ensure they are within a realistic range
        r1 = int(max(min(round(r1), 0), -100))
        r2 = int(max(min(round(r2), 0), -100))
        r3 = int(max(min(round(r3), 0), -100))
        
        # Add Tile No as 1
        synthetic_data.append([1, r1, r2, r3, human_status])
    
    # Convert to DataFrame
    synthetic_df = pd.DataFrame(synthetic_data, columns=["Tile No", "Receiver 1", "Receiver 2", "Receiver 3", "Human Status"])
    return synthetic_df

# Generate synthetic data for each human status
human_statuses = df["Human Status"].unique()
synthetic_dataframes = []

for status in human_statuses:
    # Generate synthetic data for each status (e.g., 500 samples per status)
    synthetic_df = generate_synthetic_data(df, status, num_samples=500)
    synthetic_dataframes.append(synthetic_df)

# Combine all synthetic data into one DataFrame
synthetic_data = pd.concat(synthetic_dataframes, ignore_index=True)

# Save the synthetic data to a new CSV file
synthetic_data.to_csv("synthetic_data.csv", index=False)
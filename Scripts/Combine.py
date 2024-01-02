import pandas as pd
import os

# Directory containing the TSV files
directory_path = "/ourdisk/hpc/rnafold/dywang/dont_archive/On_process/HBEC_Length_Merge/LengthAverage"

# List all TSV files in the directory
file_paths = [f for f in os.listdir(directory_path) if f.endswith('.tsv')]

# Initialize an empty DataFrame for merging
merged_df = pd.DataFrame()

# Process each file
for file_name in file_paths:
    file_path = os.path.join(directory_path, file_name)
    # Read the file
    df = pd.read_csv(file_path, sep="\t", header=None, names=["ID", "Value"])
    
    # Rename 'Value' column to the filename or a suitable identifier
    df.rename(columns={"Value": file_name}, inplace=True)

    # Merge with the main DataFrame
    if merged_df.empty:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on="ID", how="outer")

# Export the merged DataFrame
output_file = os.path.join(directory_path, "merged_output.csv")
merged_df.to_csv(output_file, sep='\t', index=False)

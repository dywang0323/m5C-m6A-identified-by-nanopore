import pandas as pd

# File paths for the input files
tpm_file_path = '/path/to/Comp_TPM_HBEC.txt'  # Replace with your actual file path
transcript_file_path = '/path/to/trascriptID.csv'  # Replace with your actual file path

# Reading the TPM data
tpm_data = pd.read_csv(tpm_file_path, sep='\t')

# Reading the transcript data
transcript_data = pd.read_csv(transcript_file_path, header=None, names=["ID", "GO_Term", "Description"])

# Merging the TPM data with the transcript data based on the ID
merged_data = pd.merge(tpm_data, transcript_data, on='ID', how='left')

# Saving the merged data to a new CSV file
output_path = '/path/to/output/merged_GO_annotations.csv'  # Replace with your desired output path
merged_data.to_csv(output_path, index=False)

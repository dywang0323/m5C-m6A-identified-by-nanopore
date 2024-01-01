import pandas as pd

def process_dataset(input_file, output_file):
    # Read the dataset
    df = pd.read_csv(input_file, sep="\t", header=None, names=["ID", "PTM"])

    # Split the ID to extract the unique identifier
    df['ID'] = df['ID'].apply(lambda x: x.split('|')[0])

    # Ensure that the PTM column contains numeric values, and handle non-numeric entries
    df['PTM'] = pd.to_numeric(df['PTM'], errors='coerce')

    # Calculate the average for each unique ID, excluding non-numeric values
    result = df.groupby('ID')['PTM'].mean().reset_index()

    # Write the result to a new file
    result.to_csv(output_file, sep="\t", index=False, header=False)

# Example usage
input_file = '/ourdisk/hpc/rnafold/dywang/dont_archive/On_process/HBEC_Length_Merge/24Nmockhbec_poliA_length.tsv'  # Replace with the path to your TSV file
output_file = '/ourdisk/hpc/rnafold/dywang/dont_archive/On_process/HBEC_Length_Merge/24Nmockhbec_poliA_length_average.tsv'             # The file to write the results to

process_dataset(input_file, output_file)

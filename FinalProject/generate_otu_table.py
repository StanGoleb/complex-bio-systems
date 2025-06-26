import pandas as pd
from pathlib import Path

def load_uc_mapping(uc_path):
    """Parses VSEARCH .uc file and returns ASV ID → OTU ID mapping."""
    asv_to_otu = {}
    with open(uc_path, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            fields = line.strip().split('\t')
            record_type = fields[0]
            cluster_num = fields[1]
            query = fields[9]
            if record_type in ('S', 'H'):
                asv_to_otu[query] = f'OTU_{cluster_num}'
    return asv_to_otu

def main():
    asv_csv = Path("initial_data/seqtable_readyforanalysis.csv")
    uc_file = Path("computed_data/otu97.uc")
    otu_out = Path("computed_data/otu_table_97.csv")

    df = pd.read_csv(asv_csv, index_col=0, sep='\t')

    if not df.columns[0].startswith("ASV_") and df.index[0].startswith("ASV_"):
        df = df.T

    asv_to_otu = load_uc_mapping(uc_file)
    df = df.loc[:, df.columns.isin(asv_to_otu)]
    df = df.rename(columns=asv_to_otu)

    df_otu = df.groupby(axis=1, level=0).sum()
    df_otu.to_csv(otu_out, index=True, index_label="SampleID")

    print(f"Saved OTU table with shape {df_otu.shape} → {otu_out}")

if __name__ == "__main__":
    main()

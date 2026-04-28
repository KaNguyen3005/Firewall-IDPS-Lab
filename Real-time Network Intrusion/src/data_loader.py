import pandas as pd
import glob

def load_data(path):
    files = glob.glob(path)
    df_list = [pd.read_csv(f) for f in files]
    return pd.concat(df_list, ignore_index=True)
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def clean_data(df):
    df.columns = df.columns.str.strip()

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(df.median(numeric_only=True), inplace=True)

    df.drop_duplicates(inplace=True)

    return df

def scale_data(X, y):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return X, y

def balance_data(X, y):
    smote = SMOTE(sampling_strategy=0.1)
    under = RandomUnderSampler()

    X, y = smote.fit_resample(X, y)
    X, y = under.fit_resample(X, y)

    return X, y
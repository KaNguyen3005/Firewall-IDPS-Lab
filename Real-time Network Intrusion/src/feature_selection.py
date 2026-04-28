from sklearn.preprocessing import LabelEncoder

def select_features(df):
    selected_features = [
        'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts',
        'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Fwd Pkt Len Mean',
        'Bwd Pkt Len Mean', 'Flow Byts/s', 'Flow Pkts/s',
        'Pkt Len Mean', 'Pkt Len Std', 'SYN Flag Cnt',
        'ACK Flag Cnt', 'FIN Flag Cnt', 'RST Flag Cnt',
        'PSH Flag Cnt', 'URG Flag Cnt'
    ]

    X = df[selected_features]

    le = LabelEncoder()
    y = le.fit_transform(df['Label'])

    return X, y
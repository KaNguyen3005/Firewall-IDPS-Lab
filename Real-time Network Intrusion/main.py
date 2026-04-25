import joblib
import pandas as pd

# ===============================
# Sample flows for different attack types
# ===============================

sample_flows = {
    "BENIGN": {
        'Destination Port': 443,
        'Flow Duration': 1200000,
        'Total Fwd Packets': 8,
        'Total Backward Packets': 7,
        'Total Length of Fwd Packets': 600,
        'Total Length of Bwd Packets': 900,
        'Fwd Packet Length Mean': 75,
        'Bwd Packet Length Mean': 128,
        'Flow Bytes/s': 1250,
        'Flow Packets/s': 12,
        'Packet Length Mean': 100,
        'Packet Length Std': 25,
        'SYN Flag Count': 1,
        'ACK Flag Count': 1,
        'FIN Flag Count': 1,
        'RST Flag Count': 0,
        'PSH Flag Count': 1,
        'URG Flag Count': 0
    },

    "DDoS": {
        'Destination Port': 80,
        'Flow Duration': 200000,
        'Total Fwd Packets': 100,
        'Total Backward Packets': 2,
        'Total Length of Fwd Packets': 60000,
        'Total Length of Bwd Packets': 100,
        'Fwd Packet Length Mean': 600,
        'Bwd Packet Length Mean': 50,
        'Flow Bytes/s': 300000,
        'Flow Packets/s': 500,
        'Packet Length Mean': 580,
        'Packet Length Std': 80,
        'SYN Flag Count': 20,
        'ACK Flag Count': 1,
        'FIN Flag Count': 0,
        'RST Flag Count': 0,
        'PSH Flag Count': 10,
        'URG Flag Count': 0
    },

    "DoS Hulk": {
        'Destination Port': 80,
        'Flow Duration': 500000,
        'Total Fwd Packets': 80,
        'Total Backward Packets': 10,
        'Total Length of Fwd Packets': 90000,
        'Total Length of Bwd Packets': 5000,
        'Fwd Packet Length Mean': 1125,
        'Bwd Packet Length Mean': 500,
        'Flow Bytes/s': 190000,
        'Flow Packets/s': 180,
        'Packet Length Mean': 1000,
        'Packet Length Std': 300,
        'SYN Flag Count': 10,
        'ACK Flag Count': 5,
        'FIN Flag Count': 0,
        'RST Flag Count': 1,
        'PSH Flag Count': 20,
        'URG Flag Count': 0
    },

    "PortScan": {
        'Destination Port': 22,
        'Flow Duration': 10000,
        'Total Fwd Packets': 2,
        'Total Backward Packets': 0,
        'Total Length of Fwd Packets': 80,
        'Total Length of Bwd Packets': 0,
        'Fwd Packet Length Mean': 40,
        'Bwd Packet Length Mean': 0,
        'Flow Bytes/s': 8000,
        'Flow Packets/s': 200,
        'Packet Length Mean': 40,
        'Packet Length Std': 5,
        'SYN Flag Count': 1,
        'ACK Flag Count': 0,
        'FIN Flag Count': 0,
        'RST Flag Count': 1,
        'PSH Flag Count': 0,
        'URG Flag Count': 0
    },

    "FTP-Patator": {
        'Destination Port': 21,
        'Flow Duration': 3000000,
        'Total Fwd Packets': 25,
        'Total Backward Packets': 20,
        'Total Length of Fwd Packets': 2000,
        'Total Length of Bwd Packets': 1500,
        'Fwd Packet Length Mean': 80,
        'Bwd Packet Length Mean': 75,
        'Flow Bytes/s': 1166,
        'Flow Packets/s': 15,
        'Packet Length Mean': 78,
        'Packet Length Std': 20,
        'SYN Flag Count': 1,
        'ACK Flag Count': 20,
        'FIN Flag Count': 1,
        'RST Flag Count': 0,
        'PSH Flag Count': 5,
        'URG Flag Count': 0
    },

    "SSH-Patator": {
        'Destination Port': 22,
        'Flow Duration': 2500000,
        'Total Fwd Packets': 20,
        'Total Backward Packets': 18,
        'Total Length of Fwd Packets': 1600,
        'Total Length of Bwd Packets': 1400,
        'Fwd Packet Length Mean': 80,
        'Bwd Packet Length Mean': 78,
        'Flow Bytes/s': 1200,
        'Flow Packets/s': 15,
        'Packet Length Mean': 79,
        'Packet Length Std': 18,
        'SYN Flag Count': 1,
        'ACK Flag Count': 18,
        'FIN Flag Count': 1,
        'RST Flag Count': 0,
        'PSH Flag Count': 4,
        'URG Flag Count': 0
    },

    "Bot": {
        'Destination Port': 8080,
        'Flow Duration': 8000000,
        'Total Fwd Packets': 15,
        'Total Backward Packets': 12,
        'Total Length of Fwd Packets': 1200,
        'Total Length of Bwd Packets': 900,
        'Fwd Packet Length Mean': 80,
        'Bwd Packet Length Mean': 75,
        'Flow Bytes/s': 260,
        'Flow Packets/s': 3,
        'Packet Length Mean': 78,
        'Packet Length Std': 15,
        'SYN Flag Count': 1,
        'ACK Flag Count': 12,
        'FIN Flag Count': 0,
        'RST Flag Count': 0,
        'PSH Flag Count': 2,
        'URG Flag Count': 0
    },

    "Web Attack - Brute Force": {
        'Destination Port': 80,
        'Flow Duration': 1500000,
        'Total Fwd Packets': 30,
        'Total Backward Packets': 25,
        'Total Length of Fwd Packets': 4000,
        'Total Length of Bwd Packets': 3000,
        'Fwd Packet Length Mean': 133,
        'Bwd Packet Length Mean': 120,
        'Flow Bytes/s': 4666,
        'Flow Packets/s': 36,
        'Packet Length Mean': 127,
        'Packet Length Std': 40,
        'SYN Flag Count': 1,
        'ACK Flag Count': 25,
        'FIN Flag Count': 1,
        'RST Flag Count': 0,
        'PSH Flag Count': 10,
        'URG Flag Count': 0
    },

    "Web Attack - XSS": {
        'Destination Port': 80,
        'Flow Duration': 1800000,
        'Total Fwd Packets': 35,
        'Total Backward Packets': 30,
        'Total Length of Fwd Packets': 5000,
        'Total Length of Bwd Packets': 3500,
        'Fwd Packet Length Mean': 142,
        'Bwd Packet Length Mean': 116,
        'Flow Bytes/s': 4722,
        'Flow Packets/s': 36,
        'Packet Length Mean': 130,
        'Packet Length Std': 45,
        'SYN Flag Count': 1,
        'ACK Flag Count': 30,
        'FIN Flag Count': 1,
        'RST Flag Count': 0,
        'PSH Flag Count': 12,
        'URG Flag Count': 0
    },

    "Web Attack - Sql Injection": {
        'Destination Port': 80,
        'Flow Duration': 2000000,
        'Total Fwd Packets': 40,
        'Total Backward Packets': 32,
        'Total Length of Fwd Packets': 6000,
        'Total Length of Bwd Packets': 4000,
        'Fwd Packet Length Mean': 150,
        'Bwd Packet Length Mean': 125,
        'Flow Bytes/s': 5000,
        'Flow Packets/s': 36,
        'Packet Length Mean': 139,
        'Packet Length Std': 50,
        'SYN Flag Count': 1,
        'ACK Flag Count': 32,
        'FIN Flag Count': 1,
        'RST Flag Count': 0,
        'PSH Flag Count': 15,
        'URG Flag Count': 0
    },

    "Infiltration": {
        'Destination Port': 4444,
        'Flow Duration': 10000000,
        'Total Fwd Packets': 12,
        'Total Backward Packets': 10,
        'Total Length of Fwd Packets': 1000,
        'Total Length of Bwd Packets': 800,
        'Fwd Packet Length Mean': 83,
        'Bwd Packet Length Mean': 80,
        'Flow Bytes/s': 180,
        'Flow Packets/s': 2,
        'Packet Length Mean': 82,
        'Packet Length Std': 12,
        'SYN Flag Count': 1,
        'ACK Flag Count': 10,
        'FIN Flag Count': 0,
        'RST Flag Count': 0,
        'PSH Flag Count': 3,
        'URG Flag Count': 0
    },

    "Heartbleed": {
        'Destination Port': 443,
        'Flow Duration': 4000000,
        'Total Fwd Packets': 50,
        'Total Backward Packets': 45,
        'Total Length of Fwd Packets': 20000,
        'Total Length of Bwd Packets': 60000,
        'Fwd Packet Length Mean': 400,
        'Bwd Packet Length Mean': 1333,
        'Flow Bytes/s': 20000,
        'Flow Packets/s': 23,
        'Packet Length Mean': 842,
        'Packet Length Std': 500,
        'SYN Flag Count': 1,
        'ACK Flag Count': 45,
        'FIN Flag Count': 0,
        'RST Flag Count': 0,
        'PSH Flag Count': 20,
        'URG Flag Count': 0
    }
}

loaded_rf_model = joblib.load("models/random_forest_best_model.pkl")
loaded_scaler = joblib.load("models/scaler.pkl")
loaded_label_encoder = joblib.load("models/label_encoder.pkl")
loaded_features = joblib.load("models/selected_features.pkl")

def simulate_realtime_flow_loaded(input_flow):
    flow_df = pd.DataFrame([input_flow])
    flow_df = flow_df[loaded_features]

    flow_scaled = loaded_scaler.transform(flow_df)

    pred_encoded = loaded_rf_model.predict(flow_scaled)
    pred_label = loaded_label_encoder.inverse_transform(pred_encoded)[0]

    destination_port = input_flow.get('Destination Port', 'Unknown')

    if pred_label != "BENIGN":
        alert_message = (
            f"[ALERT] Suspicious traffic detected: {pred_label}. "
            f"Destination Port: {destination_port}."
        )

        print(alert_message)

        with open("alerts.log", "a") as log_file:
            log_file.write(alert_message + "\n")
    else:
        print("[INFO] Normal traffic detected: BENIGN")

    return pred_label

# for expected_label, flow in sample_flows.items():
#     print("=" * 70)
#     print("Expected / Simulated Type:", expected_label)
#     predicted_label = simulate_realtime_flow_loaded(flow)
#     print("Model Prediction:", predicted_label)


simulate_realtime_flow_loaded(sample_flows["DDoS"])
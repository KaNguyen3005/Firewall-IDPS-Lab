from src.data_loader import load_data
from src.preprocessing import clean_data, scale_data, balance_data
from src.feature_selection import select_features
from src.train import train_models
from src.realtime import simulate_realtime

def main():
    df = load_data("data/*.csv")

    df = clean_data(df)

    X, y = select_features(df)

    X, y = scale_data(X, y)

    X, y = balance_data(X, y)

    model, le = train_models(X, y)

    simulate_realtime(model, le, X)

if __name__ == "__main__":
    main()
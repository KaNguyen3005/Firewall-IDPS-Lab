def simulate_realtime(model, le, X):
    sample = X[0]

    pred = model.predict([sample])[0]

    if pred != 0:
        print(f"[ALERT] Suspicious traffic detected: {pred}")
    else:
        print("Normal traffic")
def load_model(filename="kmeans_mcstat.pkl"):
    model = joblib.load(filename)
    print(f"Model loaded from {filename}")
    return model

kmeans = load_model()

def predict_mcstat(future_date):
    future_date = pd.to_datetime(future_date, format="%Y%m%d")

    last_mcstat = mcstat_tensor[-1].unsqueeze(0)

    cluster = kmeans.predict(last_mcstat)

    cluster_indices = (kmeans.predict(mcstat_tensor) == cluster).nonzero(as_tuple=True)[0]
    predicted_mcstat_numeric = torch.mode(mcstat_tensor[cluster_indices]).values.item()

    predicted_mcstat_original = encoder.inverse_transform([int(round(scaler.inverse_transform([[predicted_mcstat_numeric]])[0, 0]))])[0]

    print(f"Predicted mcstat for {future_date.date()}: {predicted_mcstat_original}")

predict_mcstat("20250415")  

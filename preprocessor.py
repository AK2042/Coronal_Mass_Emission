import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

file_name = "mcstat_data.csv"
df = pd.read_csv(file_name)

encoder = LabelEncoder()
df["mcstat_encoded"] = encoder.fit_transform(df["mcstat"])

df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
df.sort_values("Date", inplace=True)

scaler = MinMaxScaler()
df["mcstat_scaled"] = scaler.fit_transform(df["mcstat_encoded"].values.reshape(-1, 1))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mcstat_tensor = torch.tensor(df["mcstat_scaled"].values, dtype=torch.float32).to(device).unsqueeze(1) 

print("Data loaded and preprocessed.")

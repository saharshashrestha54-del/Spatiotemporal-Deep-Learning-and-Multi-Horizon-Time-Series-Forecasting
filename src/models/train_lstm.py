"""
Bidirectional LSTM (Bi-LSTM) Sequence Forecaster for Monsoon Precipitation
Project: Monsoon Precipitation Forecasting & Proactive Flood Early Warning in Nepal

Architecture:
- 2-layer Bidirectional LSTM with temporal sequence windowing (e.g., past 7 days)
- Dropout (0.2) to prevent overfitting on seasonal extremes
- Fully connected projection layer predicting multi-horizon precipitation (e.g. 24h lead)
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from src.evaluation.metrics import compute_continuous_metrics, compute_contingency_metrics


class BiLSTMForecaster(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2, dropout: float = 0.2):
        super(BiLSTMForecaster, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        # Bidirectional produces 2 * hidden_dim output
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim * 2, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        # x shape: (batch_size, seq_len, input_dim)
        lstm_out, _ = self.lstm(x)
        # Take the output of the final time step
        last_step = lstm_out[:, -1, :]
        out = self.fc(last_step)
        return out.squeeze(-1)


def create_sequences(data_features: np.ndarray, targets: np.ndarray, seq_len: int = 7):
    """Converts continuous temporal array into rolling lookback windows."""
    X, y = [], []
    for i in range(len(data_features) - seq_len):
        X.append(data_features[i:i + seq_len])
        y.append(targets[i + seq_len])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


def train_bilstm(data_path: Path, output_dir: Path, seq_len: int = 7, epochs: int = 80, lr: float = 0.005):
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(data_path)

    # Features: Precipitation and Soil Moisture
    feat_cols = ["precip_mean_mm", "soil_moisture_l1", "soil_moisture_l2", "RPI"]
    features = df[feat_cols].values
    targets = df["target_precip_lead_1d"].values

    scaler = StandardScaler()
    scaled_feats = scaler.fit_transform(features)

    X, y = create_sequences(scaled_feats, targets, seq_len=seq_len)

    split_idx = int(len(X) * 0.75)
    X_train, y_train = torch.tensor(X[:split_idx]), torch.tensor(y[:split_idx])
    X_test, y_test = torch.tensor(X[split_idx:]), torch.tensor(y[split_idx:])

    model = BiLSTMForecaster(input_dim=len(feat_cols), hidden_dim=64, num_layers=2, dropout=0.2)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)

    print(f"\n--- Training Bi-LSTM Forecaster (Lookback Window: {seq_len} days, Epochs: {epochs}) ---")
    model.train()
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        preds = model(X_train)
        loss = criterion(preds, y_train)
        loss.backward()
        optimizer.step()

        if epoch % 20 == 0 or epoch == epochs:
            print(f"Epoch [{epoch}/{epochs}] - Loss (MSE): {loss.item():.4f}")

    # Evaluation on Test Set
    model.eval()
    with torch.no_grad():
        test_preds = model(X_test).numpy()
        test_actuals = y_test.numpy()

    metrics = compute_continuous_metrics(test_actuals, test_preds)
    thresh = float(np.quantile(y[:split_idx], 0.80))
    contingency = compute_contingency_metrics(
        (test_actuals > thresh).astype(int),
        (test_preds > thresh).astype(int)
    )

    result = {
        "Model": "Bi-LSTM (2-layer, 64-dim)",
        "Lead Time": "24h",
        "RMSE (mm)": round(metrics["RMSE"], 2),
        "MAE (mm)": round(metrics["MAE"], 2),
        "KGE": round(metrics["KGE"], 2),
        "CSI": round(contingency["CSI"], 2),
        "FAR": round(contingency["FAR"], 2)
    }

    print("\n" + "=" * 70)
    print("BI-LSTM EXPERIMENTAL EVALUATION RESULTS")
    print("=" * 70)
    for k, v in result.items():
        print(f"  {k}: {v}")
    print("=" * 70)

    # Save model weights
    torch.save(model.state_dict(), output_dir / "bilstm_monsoon_24h.pt")
    print(f"Model checkpoint saved to: {output_dir / 'bilstm_monsoon_24h.pt'}")

    return result, test_actuals, test_preds


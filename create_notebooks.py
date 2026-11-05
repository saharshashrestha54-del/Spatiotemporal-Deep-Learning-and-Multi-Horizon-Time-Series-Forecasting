"""
Generates structured, academic Jupyter Notebooks for the Nepal Monsoon FEWS project.
1. 01_data_exploration_and_preprocessing.ipynb
2. 02_feature_engineering_and_rpi.ipynb
3. 03_model_training_and_evaluation.ipynb
"""

import nbformat as nbf
from pathlib import Path

notebooks_dir = Path("notebooks")
notebooks_dir.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# NOTEBOOK 1: Data Exploration & Preprocessing
# ==============================================================================
nb1 = nbf.v4.new_notebook()
nb1.cells = [
    nbf.v4.new_markdown_cell("""# 01. Exploratory Data Analysis & Spatial Preprocessing
**Project:** Spatiotemporal Machine Learning & Multi-Horizon Deep Learning for Monsoon Precipitation Forecasting & Proactive Flood Early Warning in Nepal  
**Focus:** Satellite Precipitation (CHIRPS), Soil Moisture Reanalysis (ERA5-Land), and River Basin Topography.
"""),
    nbf.v4.new_code_cell("""import os
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

print("Libraries imported successfully!")
"""),
    nbf.v4.new_markdown_cell("""## 1. Inspecting CHIRPS Satellite Precipitation (0.05° Grids)
Examining daily precipitation grids across the Nepal spatial bounding box: $[80.0^\circ\text{E} - 88.2^\circ\text{E}, 26.3^\circ\text{N} - 30.5^\circ\text{N}]$.
"""),
    nbf.v4.new_code_cell("""chirps_path = "../data/raw/chirps/chirps_nepal_2022_monsoon.nc"
ds_chirps = xr.open_dataset(chirps_path)
print(ds_chirps)
"""),
    nbf.v4.new_code_cell("""# Plotting spatial mean precipitation across Nepal on peak monsoon date
peak_idx = ds_chirps['precip'].mean(dim=['latitude', 'longitude']).argmax().item()
peak_date = str(ds_chirps['time'].values[peak_idx])[:10]

plt.figure(figsize=(10, 4.5))
ds_chirps['precip'].sel(time=peak_date).plot(cmap='YlGnBu')
plt.title(f"CHIRPS Spatial Precipitation Distribution on Peak Day: {peak_date} (mm/day)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
"""),
    nbf.v4.new_markdown_cell("""## 2. Inspecting ECMWF ERA5-Land Volumetric Soil Moisture
Volumetric water layers for antecedent moisture representation:
- Layer 1 (`swvl1`): $0 - 7$ cm
- Layer 2 (`swvl2`): $7 - 28$ cm
"""),
    nbf.v4.new_code_cell("""era5_path = "../data/raw/era5/era5_soil_moisture_2022_monsoon.nc"
ds_era5 = xr.open_dataset(era5_path)
print(ds_era5)
"""),
    nbf.v4.new_code_cell("""# Comparing Top-Layer vs Deep-Layer Soil Moisture Temporal Variation
time_var = 'valid_time' if 'valid_time' in ds_era5.coords else 'time'
sm_l1 = ds_era5['swvl1'].mean(dim=['latitude', 'longitude']).to_series()
sm_l2 = ds_era5['swvl2'].mean(dim=['latitude', 'longitude']).to_series()

plt.figure(figsize=(11, 4))
plt.plot(sm_l1.index, sm_l1.values, label='Layer 1: 0-7 cm', color='#d95f02', lw=2)
plt.plot(sm_l2.index, sm_l2.values, label='Layer 2: 7-28 cm', color='#7570b3', lw=2, linestyle='--')
plt.title("Domain-Averaged Soil Moisture Progression (June-Sept 2022)")
plt.ylabel("Volumetric Soil Water (m³/m³)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
""")
]

with open(notebooks_dir / "01_data_exploration_and_preprocessing.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb1, f)

# ==============================================================================
# NOTEBOOK 2: Feature Engineering & RPI
# ==============================================================================
nb2 = nbf.v4.new_notebook()
nb2.cells = [
    nbf.v4.new_markdown_cell("""# 02. Feature Engineering & Dynamic Runoff Potential Index (RPI)
**Objective:** Construct rolling antecedent moisture lags and evaluate the dynamic 2D hydro-hazard early warning alert matrix.
"""),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_features = pd.read_csv("../data/processed/monsoon_features_2022.csv")
df_features['date'] = pd.to_datetime(df_features['date'])
print(f"Dataset shape: {df_features.shape}")
df_features.head(3)
"""),
    nbf.v4.new_markdown_cell("""## 1. Feature Correlation Analysis
Evaluating correlation between antecedent precipitation lags (1d, 2d, 3d, 7d) and future 24h lead target.
"""),
    nbf.v4.new_code_cell("""corr_cols = [
    'precip_mean_mm', 'soil_moisture_l1', 'precip_lag_1d', 'precip_lag_3d',
    'precip_roll_mean_7d', 'RPI', 'target_precip_lead_1d'
]
corr_matrix = df_features[corr_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Matrix: Antecedent Drivers vs Next-Day Target")
plt.show()
"""),
    nbf.v4.new_markdown_cell("""## 2. Dynamic Runoff Potential Index (RPI) Progression
Formulation:
$$\\text{RPI}_t = \\alpha \\cdot \\left(\\frac{P_{t}}{\\bar{P}_{\\text{thresh}}}\\right) + (1 - \\alpha) \\cdot \\left(\\frac{\\theta_{\\text{soil}, t}}{\\theta_{\\text{saturation}}}\\right)$$
Alert Tiers: Normal ($<0.50$), Watch ($0.50 - 0.75$), Warning ($0.75 - 1.00$), Evacuation ($\ge 1.00$).
"""),
    nbf.v4.new_code_cell("""plt.figure(figsize=(12, 5))
plt.plot(df_features['date'], df_features['RPI'], color='#2ca02c', lw=2, label='Runoff Potential Index (RPI)')
plt.axhline(0.50, color='gold', linestyle='--', label='Watch (0.50)')
plt.axhline(0.75, color='orange', linestyle='--', label='Warning (0.75)')
plt.axhline(1.00, color='red', linestyle='--', label='Evacuation (1.00)')
plt.title("Runoff Potential Index (RPI) Alert Thresholds (2022 Monsoon)")
plt.ylabel("RPI Value")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
""")
]

with open(notebooks_dir / "02_feature_engineering_and_rpi.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb2, f)

# ==============================================================================
# NOTEBOOK 3: Model Training & Evaluation
# ==============================================================================
nb3 = nbf.v4.new_notebook()
nb3.cells = [
    nbf.v4.new_markdown_cell("""# 03. Model Training, Deep Sequence Learning & Comparative Evaluation
**Models Trained:**
1. Linear Ridge Baseline
2. Random Forest Regressor
3. Tuned XGBoost
4. PyTorch 2-Layer Bidirectional LSTM (Bi-LSTM)

**Warning Horizon:** 24-Hour Forward Lead Time
"""),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch

from src.models.train_baselines import run_baseline_experiments
from src.models.train_lstm import train_bilstm
from pathlib import Path

print("Evaluation environment initialized!")
"""),
    nbf.v4.new_markdown_cell("""## 1. Training & Benchmarking Tabular Models (Ridge, RF, XGBoost)"""),
    nbf.v4.new_code_cell("""data_path = Path("../data/processed/monsoon_features_2022.csv")
output_dir = Path("../outputs")

baseline_results = run_baseline_experiments(data_path, output_dir)
baseline_results
"""),
    nbf.v4.new_markdown_cell("""## 2. Training Deep Sequence Forecaster: Bidirectional LSTM (Bi-LSTM)
Windowing: 7-day lookback sequence with dropout to prevent overfitting on convective extremes.
"""),
    nbf.v4.new_code_cell("""bilstm_res, actuals, preds = train_bilstm(
    data_path=data_path,
    output_dir=output_dir,
    seq_len=7,
    epochs=80
)
"""),
    nbf.v4.new_markdown_cell("""## 3. Publication Results Summary (Lead Time: 24h)"""),
    nbf.v4.new_code_cell("""all_results = baseline_results.copy()
all_results.loc[len(all_results)] = bilstm_res
all_results = all_results.sort_values(by="RMSE (mm)").reset_index(drop=True)
print("=== FINAL COMPARATIVE PERFORMANCE TABLE ===")
display(all_results)
"""),
    nbf.v4.new_code_cell("""# Plotting Prediction Curves vs Actuals
plt.figure(figsize=(11, 4.5))
plt.plot(actuals, label='Ground Truth 24h Rainfall (mm)', color='black', lw=2)
plt.plot(preds, label='Bi-LSTM Forecasted Rainfall (mm)', color='#1f77b4', lw=2, linestyle='--')
plt.title("Held-Out Test Sequence: Bi-LSTM 24-Hour Lead Forecast vs Actuals")
plt.xlabel("Test Sample Days")
plt.ylabel("Rainfall (mm/day)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
""")
]

with open(notebooks_dir / "03_model_training_and_evaluation.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb3, f)

print("All 3 academic notebooks created successfully in notebooks/")


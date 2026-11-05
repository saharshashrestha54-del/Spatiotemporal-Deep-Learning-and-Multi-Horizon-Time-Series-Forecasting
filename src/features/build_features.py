"""
Feature Engineering and Dataset Pipeline
Project: Monsoon Precipitation Forecasting & Proactive Flood Early Warning in Nepal

Processes:
1. Spatial co-registration & alignment of CHIRPS (precipitation) and ERA5-Land (volumetric soil water).
2. Calculation of Daily Basin-Averaged Antecedent Soil Saturation and Runoff Potential Index (RPI).
3. Tabular temporal lag and rolling features (1d, 3d, 7d precipitation lags & rolling statistics) for baseline ML.
4. Export of clean, standardized feature datasets for model training & evaluation.
"""

import os
import sys
import yaml
import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path


def load_config(config_path: str = "configs/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def build_gridded_monsoon_features(
    chirps_path: Path,
    era5_path: Path,
    output_dir: Path,
    year: int = 2022
) -> pd.DataFrame:
    """
    Combines CHIRPS daily precipitation grids with ERA5-Land soil moisture layers,
    resampling/interpolating onto a common spatial grid and creating lag features.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / f"monsoon_features_{year}.csv"
    out_parquet = output_dir / f"monsoon_features_{year}.parquet"

    print(f"\n--- Loading Gridded Datasets for Year {year} ---")
    ds_chirps = xr.open_dataset(chirps_path)
    ds_era5 = xr.open_dataset(era5_path)

    # Standardize time coordinate names
    time_coord_era5 = "valid_time" if "valid_time" in ds_era5.coords else "time"
    
    # Aggregate hourly/sub-daily ERA5 to daily means to align with CHIRPS
    print("Resampling ERA5-Land soil moisture to daily frequency...")
    ds_era5_daily = ds_era5[[c for c in ['swvl1', 'swvl2'] if c in ds_era5.data_vars]].resample({time_coord_era5: "1D"}).mean()
    ds_era5_daily = ds_era5_daily.rename({time_coord_era5: "time"})

    # Ensure coordinates match: interpolate ERA5 soil moisture onto CHIRPS grid
    print("Interpolating ERA5 soil moisture to CHIRPS 0.05 deg spatial resolution...")
    era5_interp = ds_era5_daily.interp(
        latitude=ds_chirps.latitude,
        longitude=ds_chirps.longitude,
        method="linear"
    )

    # Merge variables into a unified xarray Dataset
    print("Merging precipitation and soil moisture...")
    ds_combined = xr.Dataset({
        "precip": ds_chirps["precip"],
        "soil_moisture_l1": era5_interp["swvl1"],
        "soil_moisture_l2": era5_interp["swvl2"]
    })

    # Calculate domain-averaged daily time series
    print("Extracting domain-wide daily series...")
    daily_precip = ds_combined["precip"].mean(dim=["latitude", "longitude"]).to_series()
    daily_sm_l1 = ds_combined["soil_moisture_l1"].mean(dim=["latitude", "longitude"]).to_series()
    daily_sm_l2 = ds_combined["soil_moisture_l2"].mean(dim=["latitude", "longitude"]).to_series()

    df_daily = pd.DataFrame({
        "date": daily_precip.index,
        "precip_mean_mm": daily_precip.values,
        "soil_moisture_l1": daily_sm_l1.values,
        "soil_moisture_l2": daily_sm_l2.values,
    }).dropna()

    df_daily["date"] = pd.to_datetime(df_daily["date"])
    df_daily = df_daily.sort_values("date").reset_index(drop=True)

    # Feature Engineering: Antecedent precipitation, lags, rolling stats
    print("Engineering temporal lags (1d, 2d, 3d, 7d) and rolling statistics...")
    for lag in [1, 2, 3, 5, 7]:
        df_daily[f"precip_lag_{lag}d"] = df_daily["precip_mean_mm"].shift(lag)
        df_daily[f"soil_moisture_lag_{lag}d"] = df_daily["soil_moisture_l1"].shift(lag)

    for window in [3, 7, 14]:
        df_daily[f"precip_roll_mean_{window}d"] = df_daily["precip_mean_mm"].shift(1).rolling(window).mean()
        df_daily[f"precip_roll_sum_{window}d"] = df_daily["precip_mean_mm"].shift(1).rolling(window).sum()
        df_daily[f"precip_roll_max_{window}d"] = df_daily["precip_mean_mm"].shift(1).rolling(window).max()

    # Dynamic Runoff Potential Index (RPI) Formulation (Eq. 8 in paper)
    # RPI = alpha * (Precip / Precip_95th) + (1 - alpha) * (Soil_Moisture / Soil_Saturation)
    alpha = 0.6
    p_thresh = df_daily["precip_mean_mm"].quantile(0.95)
    sm_sat = df_daily["soil_moisture_l1"].max()

    df_daily["RPI"] = alpha * (df_daily["precip_mean_mm"] / max(p_thresh, 1e-3)) + \
                      (1 - alpha) * (df_daily["soil_moisture_l1"] / max(sm_sat, 1e-3))

    # Alert Thresholds (0: Normal, 1: Watch, 2: Warning, 3: Evacuation)
    df_daily["flood_alert_level"] = 0
    df_daily.loc[df_daily["RPI"] >= 0.50, "flood_alert_level"] = 1
    df_daily.loc[df_daily["RPI"] >= 0.75, "flood_alert_level"] = 2
    df_daily.loc[df_daily["RPI"] >= 1.00, "flood_alert_level"] = 3

    # Multi-horizon forecast targets (Next 1-day, 2-day lead times)
    df_daily["target_precip_lead_1d"] = df_daily["precip_mean_mm"].shift(-1)
    df_daily["target_precip_lead_2d"] = df_daily["precip_mean_mm"].shift(-2)
    df_daily["target_flood_lead_1d"] = (df_daily["target_precip_lead_1d"] > df_daily["target_precip_lead_1d"].quantile(0.80)).astype(int)

    # Clean missing values resulting from lagging
    df_features = df_daily.dropna().reset_index(drop=True)
    df_features.to_csv(out_csv, index=False)
    print(f"Feature dataset successfully saved: {out_csv} (Shape: {df_features.shape})")

    return df_features


def process_tabular_annual_records(
    rain_csv: Path,
    soil_csv: Path,
    output_dir: Path
) -> pd.DataFrame:
    """
    Processes the annual station/grid tabular datasets (2009-2018)
    merging rainfall and soil moisture into unified spatial time series.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / "annual_basin_tabular_2009_2018.csv"

    print("\n--- Processing Annual Tabular Records (2009-2018) ---")
    df_rain = pd.read_csv(rain_csv)
    df_soil = pd.read_csv(soil_csv)

    df_merged = pd.merge(df_rain, df_soil, on=["grid_id", "Year"], how="inner")
    df_merged = df_merged.sort_values(["grid_id", "Year"]).reset_index(drop=True)

    # Calculate Grid-Level Anomalies and Rolling Historical Means
    df_merged["rain_grid_mean"] = df_merged.groupby("grid_id")["annual_rainfall_mm"].transform("mean")
    df_merged["rainfall_anomaly_pct"] = (df_merged["annual_rainfall_mm"] - df_merged["rain_grid_mean"]) / df_merged["rain_grid_mean"] * 100

    df_merged.to_csv(out_csv, index=False)
    print(f"Annual tabular features saved: {out_csv} (Shape: {df_merged.shape})")
    return df_merged


def main():
    config = load_config()
    processed_dir = Path(config["paths"]["processed_data_dir"])
    raw_dir = Path(config["paths"]["raw_data_dir"])

    chirps_2022 = raw_dir / "chirps" / "chirps_nepal_2022_monsoon.nc"
    era5_2022 = raw_dir / "era5" / "era5_soil_moisture_2022_monsoon.nc"
    rain_csv = raw_dir / "annual_rainfall_2009_2018.csv"
    soil_csv = raw_dir / "annual_soil_moisture_2009_2018.csv"

    # 1. Gridded daily pipeline (CHIRPS + ERA5)
    if chirps_2022.exists() and era5_2022.exists():
        build_gridded_monsoon_features(
            chirps_path=chirps_2022,
            era5_path=era5_2022,
            output_dir=processed_dir,
            year=2022
        )

    # 2. Annual tabular pipeline (2009-2018)
    if rain_csv.exists() and soil_csv.exists():
        process_tabular_annual_records(
            rain_csv=rain_csv,
            soil_csv=soil_csv,
            output_dir=processed_dir
        )


if __name__ == "__main__":
    main()


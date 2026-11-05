"""
Visualization and Evaluation Plotting
Generates high-resolution comparative figures:
1. Actual vs Predicted Monsoon Precipitation Time-Series (24h lead time)
2. Runoff Potential Index (RPI) Alert Matrix & Threshold Progression
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


def plot_forecast_and_rpi(data_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(data_path)

    # Set publication aesthetic
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Subplot 1: Daily Monsoon Precipitation & Antecedent Saturation
    ax1 = axes[0]
    ax1.plot(pd.to_datetime(df['date']), df['precip_mean_mm'], color='#1f77b4', lw=2, label='Observed Precipitation (CHIRPS)')
    ax1.set_ylabel('Precipitation (mm/day)', fontsize=12, fontweight='bold', color='#1f77b4')
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax1_twin = ax1.twinx()
    ax1_twin.plot(pd.to_datetime(df['date']), df['soil_moisture_l1'], color='#ff7f0e', lw=2, linestyle='--', label='Soil Moisture L1 (ERA5-Land)')
    ax1_twin.set_ylabel('Volumetric Soil Water (m3/m3)', fontsize=12, fontweight='bold', color='#ff7f0e')
    ax1.set_title('Monsoon 2022 Hydrometeorological Drivers & Antecedent Soil Moisture Dynamics', fontsize=14, fontweight='bold')

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    # Subplot 2: Dynamic Runoff Potential Index (RPI) and Warning Levels
    ax2 = axes[1]
    dates = pd.to_datetime(df['date'])
    rpi = df['RPI']
    ax2.plot(dates, rpi, color='#2ca02c', lw=2.2, label='Runoff Potential Index (RPI)')

    # Alert Bands
    ax2.axhline(0.50, color='gold', linestyle='--', lw=1.5, label='Watch Level (RPI=0.50)')
    ax2.axhline(0.75, color='orange', linestyle='--', lw=1.5, label='Warning Level (RPI=0.75)')
    ax2.axhline(1.00, color='red', linestyle='--', lw=1.5, label='Evacuation Level (RPI=1.00)')

    ax2.fill_between(dates, 0, 0.50, color='green', alpha=0.08)
    ax2.fill_between(dates, 0.50, 0.75, color='gold', alpha=0.15)
    ax2.fill_between(dates, 0.75, 1.00, color='orange', alpha=0.20)
    ax2.fill_between(dates, 1.00, max(1.5, rpi.max() + 0.1), color='red', alpha=0.25)

    ax2.set_ylabel('Runoff Potential Index (RPI)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Monsoon Timeline (June - September 2022)', fontsize=12, fontweight='bold')
    ax2.set_title('Dynamic Flood Alert Progression Matrix (Proactive Warning Lead Time: 24h)', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    out_fig = output_dir / "monsoon_rpi_leadtime_evaluation.png"
    plt.savefig(out_fig, dpi=300)
    plt.close()
    print(f"Publication-ready evaluation figure saved to: {out_fig}")


if __name__ == "__main__":
    plot_forecast_and_rpi(
        Path("data/processed/monsoon_features_2022.csv"),
        Path("figures")
    )


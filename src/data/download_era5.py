"""
ERA5-Land Reanalysis Data Acquisition Pipeline
Project: Monsoon Precipitation Forecasting & Flood Early Warning in Nepal

Downloads ERA5-Land hourly/daily reanalysis variables from the Copernicus Climate
Data Store (CDS) for the Nepal spatial domain and monsoon season.

PREREQUISITES:
    1. Create a free account at https://cds.climate.copernicus.eu/
    2. Go to your profile → API tokens
    3. Create ~/.cdsapirc with:
         url: https://cds.climate.copernicus.eu/api
         key: <your-uid>:<your-api-key>
    4. Accept the ERA5-Land licence in the CDS portal
"""

import os
import sys
import yaml
import cdsapi
from pathlib import Path
from datetime import datetime


def load_config(config_path: str = "configs/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# Variables to download and their CDS parameter names
ERA5_VARIABLES = {
    "soil_moisture": {
        "dataset": "reanalysis-era5-land",
        "variables": [
            "volumetric_soil_water_layer_1",   # 0-7 cm
            "volumetric_soil_water_layer_2",   # 7-28 cm
        ],
        "description": "Top-layer soil moisture for antecedent saturation states"
    },
    "atmospheric": {
        "dataset": "reanalysis-era5-single-levels",
        "variables": [
            "convective_available_potential_energy",  # CAPE
            "total_column_water_vapour",
        ],
        "description": "Atmospheric instability & moisture for convection"
    },
    "surface": {
        "dataset": "reanalysis-era5-land",
        "variables": [
            "total_precipitation",
            "2m_temperature",
            "surface_pressure",
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
        ],
        "description": "Surface meteorological fields"
    },
}


def download_era5_year(
    client: cdsapi.Client,
    year: int,
    variable_group: str,
    variables: list,
    dataset: str,
    bbox: dict,
    output_dir: Path,
    months: list = None,
    time_step: str = "daily",
) -> Path:
    """
    Download ERA5/ERA5-Land data for a single year and variable group.

    Args:
        client: CDS API client instance
        year: Year to download
        variable_group: Name of the variable group (for filename)
        variables: List of CDS variable names
        dataset: CDS dataset identifier
        bbox: Spatial bounding box dict from config
        output_dir: Directory to save files
        months: List of months to download (default: monsoon Jun-Sep)
        time_step: 'hourly' or 'daily'
    """
    if months is None:
        months = [6, 7, 8, 9]  # Monsoon season

    output_dir.mkdir(parents=True, exist_ok=True)
    month_label = "monsoon" if months == [6, 7, 8, 9] else "full"
    filename = f"era5_{variable_group}_{year}_{month_label}.nc"
    filepath = output_dir / filename

    if filepath.exists():
        print(f"  [SKIP] {filename} already exists.")
        return filepath

    # CDS area format: [North, West, South, East]
    area = [
        bbox["max_latitude"] + 0.2,   # North
        bbox["min_longitude"] - 0.2,  # West
        bbox["min_latitude"] - 0.2,   # South
        bbox["max_longitude"] + 0.2,  # East
    ]

    # Build month and day lists
    month_strs = [f"{m:02d}" for m in months]

    # Generate all days in the month range
    day_strs = [f"{d:02d}" for d in range(1, 32)]

    # Build time selection based on resolution
    if time_step == "hourly":
        time_list = [f"{h:02d}:00" for h in range(24)]
    else:
        # Daily aggregates: request all hours, CDS returns daily stats
        # For ERA5-Land, we request 00:00 to get daily accumulated values
        time_list = [f"{h:02d}:00" for h in range(0, 24, 3)]  # 3-hourly for manageable size

    request_params = {
        "product_type": "reanalysis",
        "variable": variables,
        "year": str(year),
        "month": month_strs,
        "day": day_strs,
        "time": time_list,
        "area": area,
        "data_format": "netcdf",
    }

    print(f"  [DOWNLOAD] {filename}")
    print(f"    Dataset:   {dataset}")
    print(f"    Variables: {variables}")
    print(f"    Period:    {year} months={month_strs}")
    print(f"    Area:      N={area[0]}, W={area[1]}, S={area[2]}, E={area[3]}")
    print(f"    Time step: {time_step} ({len(time_list)} steps/day)")

    try:
        client.retrieve(dataset, request_params, str(filepath))
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"  [OK] Saved: {filepath} ({size_mb:.1f} MB)")
        return filepath
    except Exception as e:
        print(f"  [ERROR] Failed to download {filename}: {e}")
        # Clean up partial file
        if filepath.exists():
            filepath.unlink()
        raise


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Download ERA5-Land reanalysis data for Nepal monsoon study."
    )
    parser.add_argument(
        "--mode", choices=["all", "train", "val", "test"], default="all",
        help="Which year split to download (default: all)."
    )
    parser.add_argument(
        "--years", nargs="+", type=int, default=None,
        help="Explicit list of years (overrides --mode)."
    )
    parser.add_argument(
        "--groups", nargs="+",
        choices=list(ERA5_VARIABLES.keys()) + ["all"], default=["all"],
        help="Variable groups to download (default: all)."
    )
    parser.add_argument(
        "--time-step", choices=["hourly", "daily"], default="daily",
        help="Temporal resolution (default: daily = 3-hourly samples)."
    )
    args = parser.parse_args()

    config = load_config()
    bbox = config["spatial"]["bounding_box"]
    output_dir = Path(config["paths"]["raw_data_dir"]) / "era5"
    monsoon_months = config["temporal"]["monsoon_months"]

    # Determine years
    if args.years:
        years = args.years
    elif args.mode == "train":
        s, e = config["temporal"]["train_years"]
        years = list(range(s, e + 1))
    elif args.mode == "val":
        s, e = config["temporal"]["val_years"]
        years = list(range(s, e + 1))
    elif args.mode == "test":
        years = config["temporal"]["test_years"]
    else:
        s_tr, e_tr = config["temporal"]["train_years"]
        s_v, e_v = config["temporal"]["val_years"]
        s_te, e_te = config["temporal"]["test_years"]
        years = sorted(set(
            list(range(s_tr, e_tr + 1)) +
            list(range(s_v, e_v + 1)) +
            [s_te, e_te] if isinstance(s_te, int) else config["temporal"]["test_years"]
        ))

    # Determine variable groups
    if "all" in args.groups:
        groups = list(ERA5_VARIABLES.keys())
    else:
        groups = args.groups

    print("=" * 70)
    print("ERA5-Land Reanalysis Download Pipeline")
    print("=" * 70)
    print(f"Years ({len(years)}): {years}")
    print(f"Variable groups: {groups}")
    print(f"Monsoon months: {monsoon_months}")
    print(f"Time step: {args.time_step}")
    print(f"Output: {output_dir}")
    print("=" * 70)

    # Check CDS API configuration
    cdsapirc = Path.home() / ".cdsapirc"
    if not cdsapirc.exists():
        print("\n[ERROR] ~/.cdsapirc not found!")
        print("Please create it with your Copernicus CDS credentials:")
        print("  url: https://cds.climate.copernicus.eu/api")
        print("  key: <your-uid>:<your-api-key>")
        print("\nRegister at: https://cds.climate.copernicus.eu/")
        sys.exit(1)

    client = cdsapi.Client()
    successful = []
    failed = []

    total_tasks = len(years) * len(groups)
    task_num = 0

    for year in years:
        for group_name in groups:
            task_num += 1
            group_info = ERA5_VARIABLES[group_name]
            print(f"\n[{task_num}/{total_tasks}] {group_name} — {year}")
            print(f"  {group_info['description']}")

            try:
                path = download_era5_year(
                    client=client,
                    year=year,
                    variable_group=group_name,
                    variables=group_info["variables"],
                    dataset=group_info["dataset"],
                    bbox=bbox,
                    output_dir=output_dir,
                    months=monsoon_months,
                    time_step=args.time_step,
                )
                successful.append((year, group_name, path))
            except Exception as e:
                failed.append((year, group_name, str(e)))

    # Summary
    print(f"\n{'=' * 70}")
    print("ERA5 DOWNLOAD SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Successful: {len(successful)}/{total_tasks}")
    for yr, grp, p in successful:
        print(f"    [OK] {yr}/{grp}: {p}")
    if failed:
        print(f"  Failed: {len(failed)}/{total_tasks}")
        for yr, grp, err in failed:
            print(f"    [FAIL] {yr}/{grp}: {err}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()


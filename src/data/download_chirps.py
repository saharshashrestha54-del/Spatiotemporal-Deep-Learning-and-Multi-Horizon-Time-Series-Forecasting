"""
CHIRPS v2.0 Satellite Precipitation Acquisition & Cropping Pipeline
Project: Monsoon Precipitation Forecasting & Flood Early Warning in Nepal

Downloads global daily CHIRPS NetCDF files from UCSB CHC, clips them to the Nepal
spatial bounding box specified in configs/config.yaml, and saves efficient NetCDF/Zarr files.

Supports two download strategies:
  1. Annual global NetCDF (default) — fast but large (~1 GB/year)
  2. Per-day TIFF fallback — smaller files, avoids rate limiting on large downloads
"""

import os
import sys
import time
import yaml
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm
import xarray as xr
import numpy as np


# Delay between consecutive year downloads to avoid UCSB rate limiting (seconds)
INTER_YEAR_DELAY = 30
# Max retries per file download
MAX_RETRIES = 3
# Delay between retries (seconds) — doubles each retry (exponential backoff)
RETRY_BASE_DELAY = 60


class DownloadProgressBar(tqdm):
    """Visual progress bar for urllib downloads."""
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def load_config(config_path: str = "configs/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def _download_with_retry(url: str, dest: Path, retries: int = MAX_RETRIES) -> bool:
    """Download a file with exponential backoff retry on failure."""
    for attempt in range(1, retries + 1):
        try:
            with DownloadProgressBar(unit="B", unit_scale=True, miniters=1,
                                     desc=dest.name, leave=False) as t:
                urllib.request.urlretrieve(url, filename=dest, reporthook=t.update_to)
            return True
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code == 503:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                print(f"    [RATE LIMITED] HTTP {e.code}. Waiting {delay}s before retry {attempt}/{retries}...")
                time.sleep(delay)
            elif e.code == 404:
                print(f"    [NOT FOUND] {url}")
                return False
            elif e.code == 403:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                print(f"    [FORBIDDEN] HTTP 403. Server may be rate-limiting. Waiting {delay}s...")
                time.sleep(delay)
            else:
                print(f"    [HTTP ERROR] {e.code}: {e.reason}")
                if attempt < retries:
                    time.sleep(RETRY_BASE_DELAY)
                else:
                    return False
        except Exception as e:
            print(f"    [ERROR] {e}")
            if attempt < retries:
                time.sleep(RETRY_BASE_DELAY)
            else:
                return False
    return False


def download_chirps_daily_tiffs(
    year: int,
    bbox: dict,
    output_dir: Path,
    monsoon_months: list = None,
) -> Path:
    """
    Fallback strategy: download per-day CHIRPS TIFF files and merge.
    CHIRPS daily TIFFs are much smaller (~15 MB each) and less likely to be rate-limited.

    URL pattern: https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/YYYY/
                 chirps-v2.0.YYYY.MM.DD.tif.gz
    """
    if monsoon_months is None:
        monsoon_months = [6, 7, 8, 9]

    cropped_filename = f"chirps_nepal_{year}_monsoon.nc"
    cropped_filepath = output_dir / cropped_filename

    if cropped_filepath.exists():
        print(f"  [SKIP] {cropped_filename} already exists.")
        return cropped_filepath

    temp_dir = output_dir / f"temp_daily_{year}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    base_url = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/{year}/"
    daily_files = []

    # Generate dates for monsoon months
    for month in monsoon_months:
        start = datetime(year, month, 1)
        end = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        current = start
        while current < end:
            day_str = current.strftime("%Y.%m.%d")
            tif_name = f"chirps-v2.0.{day_str}.tif.gz"
            tif_url = base_url + tif_name
            tif_path = temp_dir / tif_name

            if not tif_path.exists():
                success = _download_with_retry(tif_url, tif_path, retries=2)
                if success:
                    daily_files.append(tif_path)
                # Small delay between daily files
                time.sleep(1)
            else:
                daily_files.append(tif_path)

            current += timedelta(days=1)

    if not daily_files:
        print(f"  [ERROR] No daily files downloaded for {year}.")
        return None

    print(f"  [MERGE] Combining {len(daily_files)} daily files into {cropped_filename}...")
    try:
        # Open all daily TIFFs and merge
        datasets = []
        for f in sorted(daily_files):
            try:
                ds = xr.open_dataset(f, engine="rasterio")
                datasets.append(ds)
            except Exception:
                continue

        if datasets:
            ds_merged = xr.concat(datasets, dim="time")
            # Crop to Nepal bbox
            lat_min, lat_max = bbox["min_latitude"] - 0.2, bbox["max_latitude"] + 0.2
            lon_min, lon_max = bbox["min_longitude"] - 0.2, bbox["max_longitude"] + 0.2

            if "y" in ds_merged.dims:
                ds_cropped = ds_merged.sel(y=slice(lat_max, lat_min), x=slice(lon_min, lon_max))
            else:
                ds_cropped = ds_merged.sel(latitude=slice(lat_min, lat_max),
                                           longitude=slice(lon_min, lon_max))

            ds_cropped.to_netcdf(cropped_filepath)
            print(f"  [OK] Saved: {cropped_filepath}")

            # Cleanup temp
            for f in daily_files:
                f.unlink()
            temp_dir.rmdir()

            return cropped_filepath
    except Exception as e:
        print(f"  [MERGE ERROR] {e}")

    return None


def download_and_crop_chirps(
    year: int,
    bbox: dict,
    output_dir: Path,
    base_url: str = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/",
    monsoon_only: bool = True
) -> Path:
    """
    Downloads the annual global CHIRPS NetCDF, clips spatial bounding box,
    optionally filters for monsoon months (June-Sept), and saves the cropped file.
    Falls back to per-day TIFF downloads if annual file is unavailable.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    cropped_filename = f"chirps_nepal_{year}{'_monsoon' if monsoon_only else ''}.nc"
    cropped_filepath = output_dir / cropped_filename

    if cropped_filepath.exists():
        print(f"[{year}] Cropped file already exists: {cropped_filepath}")
        return cropped_filepath

    remote_file = f"chirps-v2.0.{year}.days_p05.nc"
    download_url = f"{base_url}{remote_file}"
    temp_download = output_dir / f"temp_{remote_file}"

    try:
        print(f"\n--- Downloading CHIRPS {year} from {download_url} ---")
        success = _download_with_retry(download_url, temp_download)

        if not success:
            print(f"[{year}] Annual NetCDF unavailable. Trying per-day TIFF fallback...")
            result = download_chirps_daily_tiffs(
                year=year, bbox=bbox, output_dir=output_dir,
                monsoon_months=[6, 7, 8, 9] if monsoon_only else list(range(1, 13))
            )
            if result:
                return result
            raise RuntimeError(f"Both annual NetCDF and daily TIFF strategies failed for {year}.")

        print(f"[{year}] Cropping to Nepal Bounding Box: {bbox}")
        # Open dataset with xarray
        with xr.open_dataset(temp_download) as ds:
            # CHIRPS coordinates: latitude ('latitude'), longitude ('longitude'), time ('time')
            lat_slice = slice(bbox["min_latitude"] - 0.2, bbox["max_latitude"] + 0.2)
            lon_slice = slice(bbox["min_longitude"] - 0.2, bbox["max_longitude"] + 0.2)

            # Check latitude orientation (CHIRPS is typically descending or ascending)
            if ds.latitude[0] > ds.latitude[-1]:
                lat_slice = slice(bbox["max_latitude"] + 0.2, bbox["min_latitude"] - 0.2)

            ds_cropped = ds.sel(latitude=lat_slice, longitude=lon_slice)

            if monsoon_only:
                print(f"[{year}] Filtering for active monsoon season (June - September)...")
                ds_cropped = ds_cropped.sel(time=ds_cropped.time.dt.month.isin([6, 7, 8, 9]))

            print(f"[{year}] Saving cropped NetCDF to {cropped_filepath}...")
            # Save cropped dataset with compression
            encoding = {"precip": {"zlib": True, "complevel": 5}}
            ds_cropped.to_netcdf(cropped_filepath, encoding=encoding)

        print(f"[{year}] Successfully generated: {cropped_filepath}")
        return cropped_filepath

    finally:
        # Cleanup large global file
        if temp_download.exists():
            temp_download.unlink()


def get_all_years(config: dict) -> list:
    """Return the full list of years from train, val, and test splits."""
    train_start, train_end = config["temporal"]["train_years"]
    val_start, val_end = config["temporal"]["val_years"]
    test_start, test_end = config["temporal"]["test_years"]
    all_years = list(range(train_start, train_end + 1)) + \
                list(range(val_start, val_end + 1)) + \
                list(range(test_start, test_end + 1))
    return sorted(set(all_years))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Download & crop CHIRPS precipitation data for Nepal."
    )
    parser.add_argument(
        "--mode", choices=["all", "train", "val", "test"], default="all",
        help="Which year split to download (default: all)."
    )
    parser.add_argument(
        "--years", nargs="+", type=int, default=None,
        help="Explicit list of years to download (overrides --mode)."
    )
    parser.add_argument(
        "--full-year", action="store_true",
        help="Download full year instead of monsoon-only (June-Sept)."
    )
    args = parser.parse_args()

    config = load_config()
    bbox = config["spatial"]["bounding_box"]
    raw_dir = Path(config["paths"]["raw_data_dir"]) / "chirps"
    base_url = config["data_sources"]["chirps"]["url_base"]

    # Determine which years to download
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
    else:  # "all"
        years = get_all_years(config)

    print(f"=" * 70)
    print(f"CHIRPS v2.0 Batch Download Pipeline")
    print(f"=" * 70)
    print(f"Config loaded. Spatial extent: {bbox}")
    print(f"Mode: {args.mode} | Monsoon-only: {not args.full_year}")
    print(f"Years to process ({len(years)}): {years}")
    print(f"Output directory: {raw_dir}")
    print(f"=" * 70)

    successful = []
    failed = []

    for i, yr in enumerate(years, 1):
        print(f"\n[{i}/{len(years)}] Processing year {yr}...")
        try:
            path = download_and_crop_chirps(
                year=yr,
                bbox=bbox,
                output_dir=raw_dir,
                base_url=base_url,
                monsoon_only=not args.full_year
            )
            successful.append((yr, path))
        except Exception as e:
            print(f"[{yr}] ERROR: {e}")
            failed.append((yr, str(e)))

        # Throttle between years to avoid UCSB rate limiting
        if i < len(years):
            print(f"\n  [THROTTLE] Waiting {INTER_YEAR_DELAY}s before next download...")
            time.sleep(INTER_YEAR_DELAY)

    # Summary
    print(f"\n{'=' * 70}")
    print(f"DOWNLOAD SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Successful: {len(successful)}/{len(years)}")
    for yr, p in successful:
        print(f"    ✓ {yr}: {p}")
    if failed:
        print(f"  Failed: {len(failed)}/{len(years)}")
        for yr, err in failed:
            print(f"    ✗ {yr}: {err}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()

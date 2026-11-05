import os
import sys
import yaml
import json
import requests
import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

def load_config(config_path: str = "configs/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_earthdata_token() -> str:
    
    token = os.environ.get("NASA_EARTHDATA_TOKEN")
    if token:
        return token.strip()

    token_file = Path.home() / ".nasa_earthdata_token"
    if token_file.exists():
        return token_file.read_text().strip()

    return None

def build_opendap_url(date: datetime, product: str = "GPM_3IMERGDF") -> str:
    
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day_of_year = date.strftime("%j")

    if product == "GPM_3IMERGDF":
        filename = f"3B-DAY.MS.MRG.3IMERG.{date.strftime('%Y%m%d')}-S000000-E235959.V07B.nc4"
        base = f"https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07/{year}/{month}/"
    elif product == "GPM_3IMERGDL":
        filename = f"3B-DAY-L.MS.MRG.3IMERG.{date.strftime('%Y%m%d')}-S000000-E235959.V07B.nc4"
        base = f"https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDL.07/{year}/{month}/"
    else:
        raise ValueError(f"Unsupported product: {product}")

    return base + filename

def download_imerg_file(
    url: str,
    output_path: Path,
    token: str,
    retries: int = 3,
) -> bool:
    
    headers = {"Authorization": f"Bearer {token}"}

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=120)

            if response.status_code == 401:
                print(f"    [AUTH ERROR] Token expired or invalid. Regenerate at Earthdata.")
                return False
            elif response.status_code == 404:
                print(f"    [NOT FOUND] {url}")
                return False

            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            with open(output_path, "wb") as f:
                with tqdm(total=total_size, unit="B", unit_scale=True,
                          desc=output_path.name, leave=False) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))
            return True

        except requests.exceptions.RequestException as e:
            if attempt < retries:
                print(f"    [RETRY {attempt}/{retries}] {e}")
            else:
                print(f"    [FAILED] {e}")
                if output_path.exists():
                    output_path.unlink()
                return False

    return False

def crop_imerg_to_nepal(
    input_path: Path,
    output_path: Path,
    bbox: dict,
    buffer_deg: float = 0.2,
) -> Path:
    
    with xr.open_dataset(input_path) as ds:
        lon_name = "lon" if "lon" in ds.coords else "longitude"
        lat_name = "lat" if "lat" in ds.coords else "latitude"

        lon_slice = slice(bbox["min_longitude"] - buffer_deg,
                          bbox["max_longitude"] + buffer_deg)
        lat_slice = slice(bbox["min_latitude"] - buffer_deg,
                          bbox["max_latitude"] + buffer_deg)

        if ds[lat_name][0] > ds[lat_name][-1]:
            lat_slice = slice(bbox["max_latitude"] + buffer_deg,
                              bbox["min_latitude"] - buffer_deg)

        ds_cropped = ds.sel({lon_name: lon_slice, lat_name: lat_slice})

        encoding = {}
        for var in ds_cropped.data_vars:
            encoding[var] = {"zlib": True, "complevel": 5}
        ds_cropped.to_netcdf(output_path, encoding=encoding)

    return output_path

def download_imerg_monsoon(
    year: int,
    bbox: dict,
    output_dir: Path,
    token: str,
    monsoon_months: list = None,
    product: str = "GPM_3IMERGDF",
    keep_global: bool = False,
) -> Path:
    
    if monsoon_months is None:
        monsoon_months = [6, 7, 8, 9]

    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir / "temp_daily"
    temp_dir.mkdir(exist_ok=True)

    merged_filename = f"imerg_{product.lower()}_{year}_monsoon.nc"
    merged_path = output_dir / merged_filename

    if merged_path.exists():
        print(f"  [SKIP] {merged_filename} already exists.")
        return merged_path

    dates = []
    for month in monsoon_months:
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        current = start
        while current < end:
            dates.append(current)
            current += timedelta(days=1)

    print(f"  Downloading {len(dates)} daily files for {year} monsoon...")

    daily_files = []
    download_count = 0
    skip_count = 0
    fail_count = 0

    for date in tqdm(dates, desc=f"IMERG {year}", unit="day"):
        url = build_opendap_url(date, product)
        daily_global = temp_dir / f"imerg_global_{date.strftime('%Y%m%d')}.nc4"
        daily_nepal = temp_dir / f"imerg_nepal_{date.strftime('%Y%m%d')}.nc"

        if daily_nepal.exists():
            daily_files.append(daily_nepal)
            skip_count += 1
            continue

        if not daily_global.exists():
            success = download_imerg_file(url, daily_global, token)
            if not success:
                fail_count += 1
                continue
            download_count += 1

        try:
            crop_imerg_to_nepal(daily_global, daily_nepal, bbox)
            daily_files.append(daily_nepal)
        except Exception as e:
            print(f"    [CROP ERROR] {date.strftime('%Y-%m-%d')}: {e}")
            fail_count += 1
            continue
        finally:
            if not keep_global and daily_global.exists():
                daily_global.unlink()

    print(f"  Downloaded: {download_count}, Skipped: {skip_count}, Failed: {fail_count}")

    if not daily_files:
        print(f"  [ERROR] No files available for {year}. Skipping merge.")
        return None

    print(f"  Merging {len(daily_files)} daily files into {merged_filename}...")
    try:
        ds_merged = xr.open_mfdataset(
            sorted(daily_files),
            combine="nested",
            concat_dim="time",
            engine="netcdf4",
        )
        encoding = {}
        for var in ds_merged.data_vars:
            encoding[var] = {"zlib": True, "complevel": 5}
        ds_merged.to_netcdf(merged_path, encoding=encoding)
        print(f"  [OK] Saved merged file: {merged_path}")

        for f in daily_files:
            if f.exists():
                f.unlink()

        return merged_path

    except Exception as e:
        print(f"  [ERROR] Failed to merge: {e}")
        return None

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Download NASA GPM IMERG precipitation data for Nepal monsoon study."
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
        "--product", choices=["GPM_3IMERGDF", "GPM_3IMERGDL"], default="GPM_3IMERGDF",
        help="IMERG product type (default: Final Daily Run)."
    )
    parser.add_argument(
        "--keep-global", action="store_true",
        help="Keep full global daily files after cropping (uses ~50MB/day)."
    )
    args = parser.parse_args()

    config = load_config()
    bbox = config["spatial"]["bounding_box"]
    output_dir = Path(config["paths"]["raw_data_dir"]) / "imerg"
    monsoon_months = config["temporal"]["monsoon_months"]

    if args.years:
        years = args.years
    elif args.mode == "train":
        s, e = config["temporal"]["train_years"]
        years = list(range(s, e + 1))
    elif args.mode == "val":
        s, e = config["temporal"]["val_years"]
        years = list(range(s, e + 1))
    elif args.mode == "test":
        s, e = config["temporal"]["test_years"]
        years = list(range(s, e + 1))
    else:
        s_tr, e_tr = config["temporal"]["train_years"]
        s_v, e_v = config["temporal"]["val_years"]
        s_te, e_te = config["temporal"]["test_years"]
        years = sorted(set(
            list(range(s_tr, e_tr + 1)) +
            list(range(s_v, e_v + 1)) +
            list(range(s_te, e_te + 1))
        ))

    print("=" * 70)
    print("NASA GPM IMERG Download Pipeline")
    print("=" * 70)
    print(f"Product:  {args.product}")
    print(f"Years ({len(years)}): {years}")
    print(f"Monsoon months: {monsoon_months}")
    print(f"Output:   {output_dir}")
    print("=" * 70)

    token = get_earthdata_token()
    if not token:
        print("\n[ERROR] NASA Earthdata token not found!")
        print("Please set it up using ONE of these methods:\n")
        print("  Method 1 — Environment variable:")
        print("    set NASA_EARTHDATA_TOKEN=<your-token>\n")
        print("  Method 2 — Token file:")
        print(f"    Save your token to: {Path.home() / '.nasa_earthdata_token'}\n")
        print("  To get a token:")
        print("    1. Register at https://urs.earthdata.nasa.gov/users/new")
        print("    2. Approve GES DISC access at https://disc.gsfc.nasa.gov/")
        print("    3. Generate token at https://urs.earthdata.nasa.gov/profile")
        sys.exit(1)

    print(f"[AUTH] Earthdata token found ({token[:8]}...)")

    successful = []
    failed = []

    for i, year in enumerate(years, 1):
        print(f"\n[{i}/{len(years)}] Processing IMERG {year} monsoon...")
        try:
            path = download_imerg_monsoon(
                year=year,
                bbox=bbox,
                output_dir=output_dir,
                token=token,
                monsoon_months=monsoon_months,
                product=args.product,
                keep_global=args.keep_global,
            )
            if path:
                successful.append((year, path))
            else:
                failed.append((year, "No data / merge failed"))
        except Exception as e:
            failed.append((year, str(e)))

    print(f"\n{'=' * 70}")
    print("IMERG DOWNLOAD SUMMARY")
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

"""
live_nav_fetch.py

Fetch historical NAV data from MFAPI for multiple mutual fund schemes
and save each scheme's NAV history as a CSV file.

Author: Rohith
Project: Mutual Fund Analytics Internship
"""

import os
import requests
import pandas as pd


# Configuration


BASE_URL = "https://api.mfapi.in/mf"

SCHEMES = {
    "SBI_Small_Cap": "125497",          # Sample scheme
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

OUTPUT_DIR = "data/raw"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)



# Function to Fetch NAV

def fetch_nav(scheme_name: str, scheme_code: str):
    """
    Fetch NAV history for a given scheme code
    and save it as a CSV.
    """

    url = f"{BASE_URL}/{scheme_code}"

    print("=" * 60)
    print(f"Fetching : {scheme_name}")
    print("=" * 60)

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        json_data = response.json()

        if json_data.get("status") != "SUCCESS":
            print(f"❌ API returned failure for {scheme_name}")
            return

        # ---------------------------
        # Metadata
        # ---------------------------

        meta = json_data.get("meta", {})

        print(f"Scheme Name : {meta.get('scheme_name')}")
        print(f"Fund House  : {meta.get('fund_house')}")
        print(f"Scheme Code : {meta.get('scheme_code')}")

        # ---------------------------
        # NAV History
        # ---------------------------

        nav_data = json_data.get("data", [])

        if not nav_data:
            print("⚠ No NAV data available.")
            return

        nav_df = pd.DataFrame(nav_data)

        # Convert date column
        nav_df["date"] = pd.to_datetime(
            nav_df["date"],
            format="%d-%m-%Y"
        )

        # Convert NAV to float
        nav_df["nav"] = nav_df["nav"].astype(float)

        # Sort oldest → newest
        nav_df = nav_df.sort_values("date")

        # Save CSV
        output_file = os.path.join(
            OUTPUT_DIR,
            f"{scheme_name}.csv"
        )

        nav_df.to_csv(output_file, index=False)

        print(f"✅ Saved : {output_file}")
        print(f"Total Records : {len(nav_df)}")

        print("\nFirst 5 Records")
        print(nav_df.head())

        print()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error : {e}")

    except requests.exceptions.ConnectionError:
        print("Connection Error")

    except requests.exceptions.Timeout:
        print("Request Timed Out")

    except requests.exceptions.RequestException as e:
        print(e)

    except Exception as e:
        print(f"Unexpected Error : {e}")


def main():
    print("\n")
    print("=" * 60)
    print("MUTUAL FUND NAV FETCHER")
    print("=" * 60)

    for scheme_name, scheme_code in SCHEMES.items():
        fetch_nav(scheme_name, scheme_code)

    print("=" * 60)
    print("All Schemes Processed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
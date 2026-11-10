
import requests
import pandas as pd
from pathlib import Path
import time

# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_URL = "https://api.worldbank.org/v2"

START_YEAR = 2000
END_YEAR = 2024

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "worldbank_global_data_2000_2024.csv"
)

INDICATORS = {
    "GDP_Current_USD": "NY.GDP.MKTP.CD",
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG",
    "GDP_Per_Capita": "NY.GDP.PCAP.CD",
    "Population": "SP.POP.TOTL",
    "Life_Expectancy": "SP.DYN.LE00.IN",
    "Health_Expenditure": "SH.XPD.CHEX.GD.ZS",
    "Agriculture_GDP": "NV.AGR.TOTL.ZS",
    "Agriculture_Employment": "SL.AGR.EMPL.ZS",
    "Cereal_Yield": "AG.YLD.CREL.KG",
    "Poverty_Rate": "SI.POV.NAHC"
}


# ==========================================
# 2. GET COUNTRY LIST
# ==========================================

def get_countries(session):

    url = f"{BASE_URL}/country"

    params = {
        "format": "json",
        "per_page": 400
    }

    response = session.get(url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()

    if not data or len(data) < 2 or data[1] is None:
        raise RuntimeError("Country list could not be retrieved.")

    countries = {}

    for country in data[1]:

        # World Bank country API uses a 3-character country ID.
        # Exclude regional and income-group aggregates.
        country_code = country.get("id")
        region = country.get("region", {}).get("id")

        if country_code and region and region != "NA":

            countries[country_code] = country["name"]

    print(f"Actual countries identified: {len(countries)}")

    return countries


# ==========================================
# 3. DOWNLOAD INDICATOR DATA
# ==========================================

def download_indicator(session, category, code, countries):

    url = f"{BASE_URL}/country/all/indicator/{code}"

    page = 1
    total_pages = 1
    records = []

    while page <= total_pages:

        params = {
            "format": "json",
            "date": f"{START_YEAR}:{END_YEAR}",
            "per_page": 20000,
            "page": page
        }

        response = session.get(url, params=params, timeout=90)
        response.raise_for_status()

        data = response.json()

        if not data or len(data) < 2 or data[1] is None:
            break

        metadata = data[0]
        observations = data[1]

        total_pages = metadata.get("pages", 1)

        for item in observations:

            country_code = item.get("countryiso3code")

            # Keep only actual countries
            if country_code not in countries:
                continue

            records.append({
                "Country_Code": country_code,
                "Country_Name": countries[country_code],
                "Year": int(item["date"]),
                "Indicator_Code": code,
                "Indicator_Name": item["indicator"]["value"],
                "Indicator_Category": category,
                "Value": item["value"]
            })

        print(f"    Page {page}/{total_pages} completed")

        page += 1

    return records


# ==========================================
# 4. MAIN FUNCTION
# ==========================================

def main():

    session = requests.Session()

    session.headers.update({
        "User-Agent": "GlobalEconomicDevelopmentAnalytics/1.0"
    })

    print("\nConnecting to World Bank API...")

    try:
        countries = get_countries(session)

    except requests.RequestException as error:
        print(f"Country download failed: {error}")
        return

    all_records = []

    # Download all indicators
    for category, code in INDICATORS.items():

        print(f"\nDownloading {category} ({code})")

        try:

            records = download_indicator(
                session,
                category,
                code,
                countries
            )

            all_records.extend(records)

            print(f"Records downloaded: {len(records):,}")

        except requests.RequestException as error:

            print(f"API error: {error}")

        time.sleep(0.5)

    # ======================================
    # 5. CREATE DATAFRAME
    # ======================================

    if not all_records:
        print("\nNo records downloaded.")
        return

    df = pd.DataFrame(all_records)

    df["Value"] = pd.to_numeric(
        df["Value"],
        errors="coerce"
    )

    df = df.sort_values(
        ["Country_Name", "Year", "Indicator_Category"]
    )

    # ======================================
    # 6. SAVE CSV
    # ======================================

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ======================================
    # 7. FINAL REPORT
    # ======================================

    print("\n" + "=" * 50)
    print("WORLD BANK DATA DOWNLOAD COMPLETED")
    print("=" * 50)

    print(f"Total records: {len(df):,}")
    print(f"Countries: {df['Country_Code'].nunique()}")
    print(f"Indicators: {df['Indicator_Code'].nunique()}")
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")

    print("\nRecords per indicator:")

    print(
        df.groupby("Indicator_Category").size()
    )

    print(f"\nCSV saved at:\n{OUTPUT_FILE}")

    print("\nDataset preview:")
    print(df.head(10).to_string(index=False))


# ==========================================
# 8. RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()


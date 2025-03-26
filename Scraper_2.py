import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

BASE_URL = "https://www.solarmonitor.org/forecast.php?date=20240324"  
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def scrape_mcstat_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    flare_table = next((table for table in tables if "MCSTAT" in table.get_text()), None)

    if not flare_table:
        print("Flare prediction table with MCSTAT not found.")
        return []

    headers = [th.get_text(strip=True) for th in flare_table.find_all("th")]
    print(f"Table headers: {headers}")

    flare_data = []
    rows = flare_table.find_all("tr")[2:]  

    for i, row in enumerate(rows, start=2):
        cols = row.find_all("td")
        if len(cols) < 50:  
            print(f"Row {i} skipped: insufficient columns ({len(cols)})")
            continue

        row_data = [col.get_text(strip=True) for col in cols]
        print(f"Row {i} data: {row_data}")

        
        if not (row_data[1].startswith(("13", "14")) and len(row_data[1]) == 5):
            print(f"Row {i} skipped: not a data row (second column: '{row_data[1]}')")
            continue

        
        noaa_numbers = []
        for j in range(1, len(row_data)):
            if row_data[j].startswith(("13", "14")) and len(row_data[j]) == 5:
                noaa_numbers.append(row_data[j])
            else:
                break
        num_regions = len(noaa_numbers)

        
        mcintosh_start = num_regions + 2  
        probs_start = mcintosh_start + num_regions + 1  

        
        mcstat_c_start = probs_start + num_regions + 1  
        mcstat_m_start = probs_start + 3 * num_regions + 3  
        mcstat_x_start = probs_start + 5 * num_regions + 5  

        mcstat_c = row_data[mcstat_c_start:mcstat_c_start + num_regions]
        mcstat_m = row_data[mcstat_m_start:mcstat_m_start + num_regions]
        mcstat_x = row_data[mcstat_x_start:mcstat_x_start + num_regions]

        for j in range(num_regions):
            try:
                data_entry = {
                    "region": noaa_numbers[j],
                    "c_class": float(mcstat_c[j]) if mcstat_c[j].isdigit() else 0.0,
                    "m_class": float(mcstat_m[j]) if mcstat_m[j].isdigit() else 0.0,
                    "x_class": float(mcstat_x[j]) if mcstat_x[j].isdigit() else 0.0,
                    "timestamp": datetime.now().isoformat()
                }
                flare_data.append(data_entry)
            except (IndexError, ValueError) as e:
                print(f"Error processing region {noaa_numbers[j]}: {e}")
                continue

    print(f"Extracted data: {flare_data}")
    return flare_data

def save_data(data, filename="flare_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    html_content = fetch_page(BASE_URL)
    if not html_content:
        return

    flare_data = scrape_mcstat_data(html_content)

    if flare_data:
        save_data(flare_data)
    else:
        print("No MCSTAT data extracted.")

if __name__ == "__main__":
    main()

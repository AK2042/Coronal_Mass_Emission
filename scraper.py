import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def scrape_mcstat(date):
    url = f"https://www.solarmonitor.org/forecast.php?date={date}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        
        mcstat_values = []
        
        for table in tables:
            for row in table.find_all("tr")[1:]:
                columns = row.find_all("td")
                if len(columns) > 5:  
                    mcstat = columns[5].text.strip()
                    if mcstat: 
                        mcstat_values.append(mcstat)

        return mcstat_values
    else:
        print(f"Failed to fetch data for {date}. Status Code:", response.status_code)
        return None

def save_to_csv(date, mcstat_values):
    file_name = "mcstat_data.csv"
    
    df = pd.DataFrame({"Date": [date] * len(mcstat_values), "mcstat": mcstat_values})
    
    try:
        existing_df = pd.read_csv(file_name)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    
    df.to_csv(file_name, index=False)
    print(f"Data for {date} saved successfully.")

today = datetime.datetime.today().strftime("%Y%m%d")
mcstat_data = scrape_mcstat(today)

if mcstat_data:
    save_to_csv(today, mcstat_data)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Electricity prices: StimaTracker
def get_table(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    soup.prettify()
    value_table = soup.find("table")
    headers = ["Period", "DC1", "DC2"]
    values = []
    for tr in value_table.find_all("tr"):
        row_data = tr.find_all("td")
        row = [i.text for i in row_data[:3]]
        values.append(row)
    df = pd.DataFrame(values, columns=headers)
    df["Period"] = pd.to_datetime(df["Period"])
    df.drop([0, 1, 2], axis=0, inplace=True)
    df.drop("DC1", axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

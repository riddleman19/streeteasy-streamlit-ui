# At top of script
import streamlit as st

if st.sidebar.button("Scrape"):
    urls = st.sidebar.text_area("URLs, one per line").splitlines()
    df = pd.DataFrame([scrape_listing(u) for u in urls])
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "data.csv")
# streeteasy_scraper.py
# This script scrapes listings from StreetEasy and saves the data to a CSV file.
# It extracts apartment features, building features, and neighborhood features from the listing descriptions.
# Usage: python streeteasy_scraper.py <url1> <url2> ... 


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_listing(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    # Grab the main description container (adjust as necessary)
    overview_div = soup.find('div', class_='overview') or soup.find('div', class_='styles__ContentWrapper')
    text = overview_div.get_text(" ").strip() if overview_div else ''

    # Segment based on key transitional phrases
    apt = bdg = nbhd = ''
    apt_match = re.search(r"each apartment features (.*?)(?:\.)", text, re.IGNORECASE)
    bdg_match = re.search(r"(?:amenities include|services that)(.*?)(?:\.)", text, re.IGNORECASE)
    nbhd_match = re.search(r"nestled in (.*?)(?:\.|$)", text, re.IGNORECASE)

    if apt_match: apt = apt_match.group(1).strip()
    if bdg_match: bdg = bdg_match.group(1).strip()
    if nbhd_match: nbhd = nbhd_match.group(1).strip()

    return {"URL": url, "Apartment Features": apt, "Building Features": bdg, "Neighborhood Features": nbhd}

def run(urls, output_csv='listings.csv'):
    rows = [scrape_listing(url) for url in urls]
    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(df)

if __name__ == "__main__":
    import sys
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python scraper.py <url1> <url2> ...")
    else:
        run(urls)

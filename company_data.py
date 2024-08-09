# import modules
import requests
import pandas as pd
from connection import conn
from headers import headers
from bs4 import BeautifulSoup

def get_cik_list():
    '''Function to get all companies tickers from SEC database'''
    print("Fetching CIK list from SEC database...")
    companyTickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers
        )
    company_data = pd.DataFrame.from_dict(companyTickers.json(), orient="index")
    company_data.columns = ['cik', 'ticker', 'title']
    company_data['cik'] = company_data['cik'].astype(str).str.zfill(10)
    cik_list = company_data['cik'].to_list()
    
    print(f"Retrieved {len(cik_list)} CIKs.")
    return cik_list

def check_filings(cik):
    '''Function to check if company has filed in FY 2023
    Returns:
    -Company metadata in dictionary format
    -Form 10K metadata for FY 2023'''
    print(f"Checking filings for CIK: {cik}...")
    filingMetadata = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=headers)
    filings = filingMetadata.json()

    comp_keys = ['cik', 'name', 'tickers', 'ein']
    filings_meta = {k: v for k, v in filings.items() if k in comp_keys}
    filings_meta['cik'] = filings_meta['cik'].zfill(10)
    if filings_meta['tickers']:
        filings_meta['tickers'] = filings_meta['tickers'][0]
    else:
        filings_meta['tickers'] = ""
    
    allforms = pd.DataFrame(filingMetadata.json()['filings']["recent"])
    allforms = allforms[allforms['form'] == "10-K"]
    allforms = allforms[(allforms['reportDate'] > "2023-01-01") & (allforms['reportDate'] < "2024-01-01")]

    if allforms.empty:
        print(f"No 10-K filings found for CIK: {cik}.")
        return None, None, None

    allforms = allforms[['accessionNumber', 'reportDate', 'form', 'primaryDocument']]
    allforms.insert(0, "cik", filings_meta['cik'])
    allforms.reset_index(drop=True, inplace=True)
    
    form_dict = allforms.to_dict(orient="records")
    
    print(f"Found {len(form_dict)} 10-K filings for CIK: {cik}.")
    return filings_meta, allforms, form_dict

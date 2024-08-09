import requests
from company_data import check_filings
from filter_data import filter_xml_content
from headers import headers
import xmltodict

from process_data import process_text_entries

def get_form_data(form_list):
    print("Generating URLs and SCF CIK list...")
    base_url = "https://www.sec.gov/Archives/edgar/data/{}/{}/{}.xml"
    urls = []
    scf_cik_list = []
    for form_meta in form_list:
        for form in form_meta:
            cik = str(form["cik"]).lstrip("0")
            accessionNumber = form["accessionNumber"].replace("-", "")
            doc_link = form["primaryDocument"].replace(".", "_")
            url = base_url.format(cik, accessionNumber, doc_link)
            urls.append(url)
            scf_cik_list.append(cik.zfill(10))
    print(f"Generated {len(urls)} URLs and SCF CIKs.")
    return urls, scf_cik_list

def fetch_data(url):
    print(f"Fetching data from URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        if url.endswith('.json'):
            return response.json()
        else:
            return xmltodict.parse(response.content)
           
    except requests.exceptions.RequestException as e:
        print(f"Request error for URL {url}: {e}")
        return None
    
def fetch_and_parse_xml(urls):
    print("Fetching and parsing XML data...")
    return [fetch_data(url) for url in urls]

def process_form_data(urls, cik):
    name = None
    print(f"Processing form data for CIK: {cik}...")
    keywords = [r'supplierfinanceprogram.*textblock']   # Keywords to filter the document
    entries = []
    for url in urls:
        print(f"Processing URL: {url}")
        xml_data = fetch_data(url)
        if xml_data is None:
            print(f"No data returned for URL: {url}")
            entries.append({"scf_flag": 0, "Name": name, "Content": None})
            continue
        
        filtered_results = filter_xml_content(xml_data, keywords)
        if filtered_results:
            print(f"Filtered results found for URL: {url}")
            for k, v in filtered_results:
                if isinstance(v, dict) and '#text' in v:
                    data_dict = process_text_entries(v["#text"])
                    entries.append({"scf_flag": 1, "Name": name, "Content": data_dict})
        else:
            print(f"No filtered results found for URL: {url}")
            entries.append({"scf_flag": 0, "Name": name, "Content": None})
    
    print(f"Processed {len(entries)} entries for CIK: {cik}.")
    return entries

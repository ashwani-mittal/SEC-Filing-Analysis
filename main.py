from company_data import check_filings, get_cik_list
from form_data import get_form_data, process_form_data
from insert_sql import insert_data

def main():
    print("Starting main function...")
    
    # Get the list of CIKs
    print("Getting list of CIKs...")
    cik_list = get_cik_list()
    form_data_list = []
    company_data_list = []
    
    # Process each CIK
    print("Processing each CIK...")
    for cik in cik_list:
        comp_data, form_data_flag, form_data = check_filings(cik)
        if form_data_flag is not None:
            company_data_list.append(comp_data)
            form_data_list.append(form_data)
    
    print(f"Company data list: {len(company_data_list)} entries")
    print(f"Form data list: {len(form_data_list)} entries")
    
    # Get form data URLs and SCF CIKs
    print("Getting form data URLs and SCF CIKs...")
    urls, scf_ciks = get_form_data(form_data_list)
    
    all_data = {}
    print("Processing form data for each URL...")
    for i, url in enumerate(urls):
        cik = scf_ciks[i]
        entries = process_form_data([url], cik)
        if cik not in all_data:
            all_data[cik] = []
        all_data[cik].extend(entries)
    
    print(f"All data processed for {len(all_data)} CIKs")
    
    # Insert data into the database or desired storage
    print("Inserting data into the database...")
    insert_data(company_data_list, form_data_list, all_data)
    
    print("Main function execution completed.")

if __name__ == "__main__":
    main()
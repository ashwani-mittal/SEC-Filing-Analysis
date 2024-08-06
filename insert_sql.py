from connection import conn
from datetime import datetime
from process_data import final_process
import json

has_run_sql_insert = False

# Function to connect to MySQL and insert data
def insert_data(company_data_list, form_data_list, all_data):
    try:
        print("Connecting to MySQL...")
        # Connect to MySQL
        cursor = conn.cursor()

        print("Inserting CompanyData...")
        # Insert CompanyData
        for company_data in company_data_list:
            cik = company_data['cik']
            # Check if CIK already exists
            cursor.execute("SELECT * FROM company_data WHERE cik = %s", (cik,))
            existing_company = cursor.fetchone()
            if not existing_company:
                cursor.execute("INSERT INTO company_data (cik, ticker, title, EIN) VALUES (%s, %s, %s, %s)", (cik, company_data['tickers'], company_data['name'], company_data['ein']))
                print(f"Inserted CompanyData for CIK: {cik}")

        print("Inserting FormData...")
        # Insert FormData with CIK as foreign key
        for form_data in form_data_list:
            for entry in form_data:
                cik = entry['cik']
                reportDate = datetime.strptime(entry['reportDate'], "%Y-%m-%d").date()
                cursor.execute("SELECT * FROM form_data WHERE cik = %s", (cik,))
                existing_company = cursor.fetchone()
                if not existing_company:
                    cursor.execute("INSERT INTO form_data (cik, accensionNumber, reportDate, form, doc_link) VALUES (%s, %s, %s, %s, %s)", (cik, entry['accessionNumber'], reportDate, entry['form'], entry['primaryDocument']))
                    print(f"Inserted FormData for CIK: {cik}")

        print("Inserting SCF Data...")
        # Insert df_all_data into scf_data table
        df_all_data = final_process(all_data)  # Call final_process to get the DataFrame
        
        for index, row in df_all_data.iterrows():
            json_string = json.dumps(row['Table'])
            cik = row['CIK']
            cursor.execute("SELECT * FROM scf_data WHERE cik = %s", (cik,))
            existing_company = cursor.fetchone()
            if not existing_company:
                cursor.execute("INSERT INTO scf_data (cik, supplier_financing_program, text_content, table_content) VALUES (%s, %s, %s, %s)", (row['CIK'], row['Supplier Financing Program'], row['Text'], json_string))
                print(f"Inserted SCF Data for CIK: {cik}")

        # Commit changes to the database
        conn.commit()
        print("Data inserted successfully.")

    except conn.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

from bs4 import BeautifulSoup
import pandas as pd

def process_text_entries(html_content):
    print("Processing text entries...")
    all_data = []
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    if table:
        table_data = []
        rows = table.find_all('tr')
        for row in rows[1:]:
            row_data = [data.get_text().strip() for data in row.find_all('td')]
            table_data.append(row_data)
        # Store only the text content outside of the table
        text_content = soup.find_all(text=True, recursive=True, exclude=["table", "thead", "tbody", "tfoot"])
        text_content = "".join([text.strip() for text in text_content if text.strip()])
        if text_content == "":
            all_data.append({'Text': None, 'Table': table_data})
        else:
            all_data.append({'Text': text_content, 'Table': table_data})
    else:
        text_content = soup.get_text().strip()
        all_data.append({'Text': text_content, 'Table': None})
    print(f"Processed entries: {len(all_data)}")
    return all_data

def final_process(all_data):
    print("Starting final process...")
    df_rows = []
    for cik, entries in all_data.items():
        for entry in entries:
            flattened_entry = {'CIK': cik, 'Supplier Financing Program': entry['Key']}
            
            # Flatten the 'Content' column if it exists and is not None
            if 'Content' in entry and entry['Content'] is not None:
                content_data = entry['Content']
                if len(content_data) > 0:
                    content_dict = content_data[0]  # Assuming only one dictionary in 'Content'
                    flattened_entry.update(content_dict)
                else:
                    content_dict = {}  # If Content is empty, store an empty dictionary
                    flattened_entry.update(content_dict)
            else:
                # If 'Content' key does not exist, store None in the columns
                flattened_entry.update({
                    'Text': None,
                    'Table': None,
                })           
            df_rows.append(flattened_entry)

    # Create DataFrame from list of dictionaries (df_rows)
    print(f"Creating DataFrame with {len(df_rows)} rows")
    df_all_data = pd.DataFrame(df_rows)
    print("Final process completed.")
    return df_all_data
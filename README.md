# Project: Create database of firms that participate in reverse factoring and the obligations filed under ASU 2022 #

*This is project to create a database of firms that filed their 10-Ks with the SEC in FY 2023.* 

- The first step is scraping the SEC EDGAR Database to get a list of all company ciks[unique indentifier] and then, parsing the company and form metadata for FY 2023 and 10-K filings. 
- We then parse the filings and filter to look for Supplier financing obligations in the Notes to Consolidated Statements section of the 10-K document.
-  The final step is storing the data in a SQL Database sec_filing. The database has 3 tables, namely, 
    * company_data: Details of the firm 
    * form_data: Metadata of the filing
    * scf_data: Data about firms and reverse factoring


Steps to Execute: 
- Run the Create_Database.sql file in MySQL Server to generate the database schema before executing the code
- Update connection.py file with your MySQL credentials 
- Update headers.py file with your name and email
- Run main.py file
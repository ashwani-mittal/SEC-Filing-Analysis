CREATE DATABASE sec_filing;
USE sec_filing;

CREATE TABLE company_data (
    cik VARCHAR(10) PRIMARY KEY,
    ticker VARCHAR(10),
    title VARCHAR(255),
    EIN VARCHAR(20)
);

CREATE TABLE form_data (
    cik VARCHAR(10),
    accensionNumber VARCHAR(50),
    reportDate VARCHAR(255),
    form VARCHAR(20),
    doc_link VARCHAR(100),
    FOREIGN KEY (cik) REFERENCES company_data(cik)
);

CREATE TABLE scf_data (
    cik VARCHAR(10),
    company_name VARCHAR(255),
    supplier_financing_program VARCHAR(50),
    text_content TEXT,
    table_content TEXT
);
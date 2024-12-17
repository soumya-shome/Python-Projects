import fitz  # PyMuPDF
import pdfplumber
import pandas as pd

def read_password_protected_pdf(file_path, password):
    # Open the PDF file
    pdf_document = fitz.open(file_path)
    
    # Check if the PDF is encrypted
    if pdf_document.is_encrypted:
        # Try to authenticate with the provided password
        if not pdf_document.authenticate(password):
            raise ValueError("Incorrect password")
    
    # Extract tables from each page and store them in a list of dataframes
    tables = []
    found_heading = False
    with pdfplumber.open(file_path, password=password) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            print(text)
            # Check if the heading "HOLDINGS BALANCE As on 2024-12-16" is in the text
            if "HOLDINGS BALANCE" in text in text:
                found_heading = True
            
            # If the heading has been found, extract tables from the subsequent pages
            if found_heading:
                tables_on_page = page.extract_tables()
                for table in tables_on_page:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    tables.append(df)
                break  # Stop after finding the first table after the heading
    
    return tables

# Example usage
file_path = "Transactions_Holdings_Statement_1663348223_01-03-2024_16-12-2024.pdf"
password = "OBCPS3177P"

try:
    tables = read_password_protected_pdf(file_path, password)
    # print(tables[1])
    holdings  = tables[1]
    
    # holdings.rename(columns={'Safe\nKeep\nBal': 'Safe\nKeep\nBal'.replace('\n',' ')}, inplace=True)
    for i in holdings.columns:
        if '\n' in i:
            holdings.rename(columns={i: i.replace('\n',' ')}, inplace=True)
    print(holdings)
    # for i, table in enumerate(tables):
    #     print(f"Table {i+1}:\n{table}\n")
except ValueError as e:
    print(e)
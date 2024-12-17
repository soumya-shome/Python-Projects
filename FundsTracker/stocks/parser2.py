import fitz
import pandas as pd

def extract_table_from_protected_pdf(pdf_path, password):
  """Extracts tables from a password-protected PDF file using PyMuPDF and returns them as Pandas DataFrames.

  Args:
      pdf_path (str): Path to the PDF file.
      password (str): Password to decrypt the PDF.

  Returns:
      list: A list of Pandas DataFrames, one for each table in the PDF.
  """

  with open(pdf_path, "rb") as f:
    try:
      # Try using fitz.open() for newer versions
      doc = fitz.open(f, password=password)
    except TypeError:  # Handle the case where password argument is not supported
      doc = fitz.openpdf(f, password=password)
    tables = []

    for page_num in range(doc.page_count):
      page = doc[page_num]
      page_tables = page.find_tables()

      for table in page_tables.tables:
        df = table.to_pandas()
        tables.append(df)

    doc.close()
    return tables

if __name__ == "__main__":
  pdf_file = "Transactions_Holdings_Statement_1663348223_01-03-2024_16-12-2024.pdf"
  password = "OBCPS3177P"
  tables = extract_table_from_protected_pdf(pdf_file, password)

  # Print the first table as an example
  if tables:
    print(tables[0])
  else:
    print("No tables found in the PDF.")
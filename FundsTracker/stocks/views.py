# from django.shortcuts import render
# import fitz  # PyMuPDF

# def read_password_protected_pdf(file_path, password):
#     # Open the PDF file
#     pdf_document = fitz.open(file_path)
    
#     # Check if the PDF is encrypted
#     if pdf_document.is_encrypted:
#         # Try to authenticate with the provided password
#         if not pdf_document.authenticate(password):
#             raise ValueError("Incorrect password")
    
#     # Extract text from each page
#     text = ""
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document.load_page(page_num)
#         text += page.get_text()
    
#     return text

# # Example usage
# file_path = "Transactions_Holdings_Statement_1663348223_01-03-2024_16-12-2024.pdf"
# password = "OBCPS3177P"

# try:
#     pdf_text = read_password_protected_pdf(file_path, password)
#     print(pdf_text)
# except ValueError as e:
#     print(e)
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
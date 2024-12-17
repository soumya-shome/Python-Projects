from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import os
import pandas as pd
import json

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
            # print(text)
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

def home(request):
    # Path to the JSON file
    json_file_path = 'holdings.json'
    
    try:
        # Read JSON file line by line and convert to DataFrame
        with open(json_file_path, 'r') as file:
            data = [json.loads(line) for line in file]
        df = pd.DataFrame(data)
        
        # Convert DataFrame to HTML table
        html_table = df.to_html()
        
    except FileNotFoundError:
        # Handle file not found error
        html_table = "<p>No data found</p>"
    except json.JSONDecodeError as e:
        return HttpResponse(f"JSONDecodeError: {e}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    
    return render(request, 'home.html', {'html_table': html_table})

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        textfield1 = request.POST.get('textfield1')
        dropdown = request.POST.get('dropdown')
        
        # Create the 'uploads' directory if it doesn't exist
        uploads_dir = 'uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Save the uploaded file to the 'uploads' directory
        file_path = os.path.join(uploads_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # # Read the content of the file
        # with open(file_path, 'r') as file:
        #     file_content = file.read()

        try:
            # Read the password-protected PDF and extract tables
            tables = read_password_protected_pdf(file_path, textfield1)
            holdings = tables[1]
            
            # Rename columns to remove newline characters
            for i in holdings.columns:
                if '\n' in i:
                    holdings.rename(columns={i: i.replace('\n', ' ')}, inplace=True)
            
            # Print the DataFrame to check the structure
            # print(holdings)
            holdings = holdings[['ISIN Code','Company Name','Current Bal','Rate','Value']]
            holdings = holdings.drop(holdings.index[-1])
            # Convert DataFrame to JSON with each record on a new line
            holdings.to_json('holdings.json', orient='records', lines=True)

        except ValueError as e:
            print(e)
        
        # Delete the file after reading its content
        os.remove(file_path)
        
        # # Prepare the response data
        # response_data = {
        #     'file_name': uploaded_file.name,
        #     'file_content': file_content,
        #     'textfield1': textfield1,
        #     'dropdown': dropdown
        # }
        
        # return JsonResponse(response_data)
        return redirect('home')
    
    return render(request, 'upload.html')
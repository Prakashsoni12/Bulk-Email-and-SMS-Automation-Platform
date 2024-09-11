from django.shortcuts import render,HttpResponse
import re
import csv
import pandas as pd
from PyPDF2 import PdfReader
import pdfplumber


# Create your views here.


def home(request):
    return render(request,"index.html")

 # Function to extract emails from text content
def extract_emails(text):
      # Regular expression to find email addresses
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_regex, text)


 # Read emails from .txt file
def read_txt_file(file_path):
    emails = []
    with open(file_path, 'r') as file:
        content = file.read()
        emails = extract_emails(content)
        return emails

        # Read emails from .csv file
def read_csv_file(file_path):
    emails = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
                row_text = ' '.join(row)  # Combine all columns into a single string
                emails.extend(extract_emails(row_text))
        return emails

        # Read emails from .xlsx (Excel) file
def read_excel_file(file_path):
    emails = []
    df = pd.read_excel(file_path)
    for col in df.columns:
        df[col] = df[col].astype(str)  # Convert all data to string to handle numeric data
        emails.extend(extract_emails(' '.join(df[col].values)))
    return emails

        # Read emails from .pdf file using PyPDF2
def read_pdf_file(file_path):
    emails = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        emails.extend(extract_emails(text))
    return emails

        # Alternative: Read emails from .pdf file using pdfplumber (more accurate for some PDFs)
def read_pdf_file_pdfplumber(file_path):
    emails = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            emails.extend(extract_emails(text))
    return emails


def recevie_mail(request):
  
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
       
        # Function to process multiple files
        def extract_emails_from_files(file_paths):
            all_emails = set()  # Use a set to avoid duplicate emails
            for file_path in file_paths:
                if file_path.endswith('.txt'):
                    all_emails.update(read_txt_file(file_path))
                elif file_path.endswith('.csv'):
                    all_emails.update(read_csv_file(file_path))
                elif file_path.endswith('.xlsx'):
                    all_emails.update(read_excel_file(file_path))
                elif file_path.endswith('.pdf'):
                    all_emails.update(read_pdf_file_pdfplumber(file_path))  # Using pdfplumber here
            return all_emails

            
        emails = extract_emails_from_files(uploaded_file)
            
        if emails:
            print("Extracted emails:")
            for email in emails:
                print(email)
            else:
                print("No emails found.")


    return render
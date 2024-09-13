import re
import csv
import pandas as pd
from PyPDF2 import PdfReader
import pdfplumber
 

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
import csv

def read_csv_file(uploaded_file):
    emails = []
    uploaded_file.seek(0)  # Reset file pointer to the start
    reader = csv.reader(uploaded_file.read().decode('utf-8').splitlines())  # Decode the file content
    
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
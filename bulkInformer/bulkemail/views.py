from django.shortcuts import render,HttpResponse,redirect
from django.core.mail import send_mail,send_mass_mail
import re
from .fileprocess import read_csv_file,read_excel_file
# Create your views here.


def home(request):
    return render(request,"index.html")



  # Function to process multiple files
def extract_emails_from_files(file):
    emails = set()
    # Check the file type and process accordingly
    if file.name.endswith('.txt'):
        for line in file:
            emails.update(re.findall(r'[\w\.-]+@[\w\.-]+', line.decode()))
            
    elif file.name.endswith('.pdf'):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                emails.update(re.findall(r'[\w\.-]+@[\w\.-]+', text))
        except ImportError as e:
            return str(e)  # PDF handling requires PyPDF2
        
    elif file.name.endswith('.xlsx'):
       xlx =  read_excel_file(file)
       emails.update(xlx)

    elif file.name.endswith('.csv'):
        csvfile = read_csv_file(file)
        emails.update(csvfile)
    else:
        return "No file found"
    return list(emails)

#this function will display output on webpage
def file_upload_view(request):
    if request.method == "POST":
        file = request.FILES['file']
            
        emails = extract_emails_from_files(file)
        return render(request,"index.html",{'emails':emails})

    return render(request,"index.html")

def send_emails(request):
    if request.method == 'POST':
        emails = request.POST.getlist('emails')
        

    return 

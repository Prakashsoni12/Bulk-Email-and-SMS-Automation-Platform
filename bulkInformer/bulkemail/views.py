from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.core.mail import send_mail,send_mass_mail
import re
from .fileprocess import read_csv_file,read_excel_file
from .task import send_bulk_emails
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
        from_email = request.POST.get("emailfrom")
        to_email = request.POST.get("emailto")
        to_subject = request.POST.get("subject")
        to_message = request.POST.get("message")
        file = request.FILES.get('file')

        if not  from_email or not to_email or not to_subject or not to_message:
            messages.error(request,'Please fill all the required fileds')
            return render(request,'index.html')
        
        if not file:
            try:
                send_mail(to_subject, to_message, from_email, [to_email])
                messages.success(request, f'Email sent to {to_email}')
            except Exception as e:
                messages.error(request,f'Failed to send to: {str(e)}')
        else:
            emails = extract_emails_from_files(file)
            return render(request,"index.html",{'emails':emails})

    return render(request,"index.html")

def send_emails(request):
    if request.method == 'POST':
        emailsa = request.POST.getlist('emails')

        send_bulk_emails.delay(emailsa)
        return render(request,'index.html',{'emailsa':emailsa})

    return redirect('file_upload_view')

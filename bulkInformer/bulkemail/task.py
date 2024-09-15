from django.core.mail import send_mail,send_mass_mail
from django.core.mail import send_mail

def send_bulk_emails(email_list):
    subject = 'your subject here'
    messsage = 'this is the body of the email.'
    from_email = 'yourmail@gmail.som'

    for email in email_list:
        send_mail(subject,messsage,from_email, [email])

    return f'Sent emails to {len(email_list)} recipients.'

from passlib.context import CryptContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import settings_email

# hasing the pass
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# hasing credentials
def verify_pass(plain_pass, hased_pass):
    return pwd_context.verify(plain_pass, hased_pass)

def send_contact_email(contact):
    msg = MIMEMultipart()
    msg['From'] = settings_email.EMAIL_FROM
    msg['To'] = settings_email.EMAIL_TO
    msg['Subject'] = "New Contact Message"

    body = f"""
    New contact message received:
    
    Name: {contact.name}
    Email: {contact.email}
    Phone: {contact.phone_nr}
    Message: {contact.message}
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(settings_email.EMAIL_HOST, settings_email.EMAIL_PORT)
        server.starttls()
        server.login(settings_email.EMAIL_HOST_USER, settings_email.EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings_email.EMAIL_FROM, settings_email.EMAIL_TO, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
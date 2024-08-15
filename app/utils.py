from passlib.context import CryptContext
import smtplib

# hasing the pass
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# hasing credentials
def verify_pass(plain_pass, hased_pass):
    return pwd_context.verify(plain_pass, hased_pass)

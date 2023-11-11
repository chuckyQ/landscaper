import secrets
import string

alphabet = string.ascii_letters + string.digits

def generate_password():

    return ''.join(secrets.choice(alphabet) for i in range(16))

import random

def generate_otp():
    return str(random.randint(100000,999999))


def verify_otp(sent_otp):

    user_otp = input("Enter OTP: ")

    if user_otp == sent_otp:
        return True
    
    return False
import math
import random
import pyotp

def generate_otp_code():
    string = '0123456789'
    OTP = ''
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]
    return OTP

def verify_otp(secret, code):
    totp = pyotp.TOTP(secret)
    is_verified = totp.verify(code)
    return is_verified

def verify_two_factor(secrect, code):
    totp = pyotp.TOTP(secrect)
    is_verified = totp.verify(code)
    return is_verified
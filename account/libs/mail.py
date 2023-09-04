from django.core.mail import EmailMessage

def send_mail(mail_subject, body, mail_to):
    email = EmailMessage(
        subject = mail_subject,
        body = body,
        to = [mail_to]
    )
    try:
        email.send()
        return True
    except Exception as ex:
        print(ex)
        return False
    
def send_mail_with_otp(otp, mail_to):
    subject = ' OTP for login'
    body = 'Your OTP is ' + otp
    if send_mail(subject, body, mail_to):
        return True
    else:
        return False
    
def send_mail_with_link_reset_password(user, ip, ticket):
    subject = f'Password reset on {ip}'
    body = f'Please go to the following page and choose a new password: \n http://127.0.0.1:8000/accounts/reset/tk/{ticket}'
    if send_mail(subject, body, user.email):
        return True
    else:
        return False
from django.core.mail import EmailMessage
import threading

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
    send_mail_user_threading(subject, body, mail_to).start()
    
def send_mail_with_link_reset_password(user, ip, ticket):
    subject = f'Password reset on {ip}'
    body = f'Please go to the following page and choose a new password: \n http://127.0.0.1:8000/accounts/reset/tk/{ticket}'
    send_mail_user_threading(subject,body, user.email).start()
    
def send_mail_user_threading(subject,body, mail_to):
    email_thread = threading.Thread(target=send_mail, args=(subject, body, mail_to))
    return email_thread
    
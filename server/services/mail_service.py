from flask_mailman import EmailMessage

def create_email(email, url):
    msg = EmailMessage()
    msg.subject = "Password Reset"
    msg.from_email = 'bentohdev@gmail.com'
    msg.to = [email]
    msg.body = f'''To reset your password, please visit this URL:\n 
            
    {url}\n

    If you didn't request for a password reset, please ignore this message.
    
    '''
    
    return msg

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


from dotenv import load_dotenv

load_dotenv()


def send_email(content: str):
    '''
    Sends an email using SendGrid.    
    This method expects the content of the email to be passed as an argument.
    The content needs to be in HTML format.
    The content needs to mention the product name and price and the difference in price.    
    '''
    
    message = Mail(
        from_email=os.environ.get('FROM_EMAIL'),
        to_emails=os.environ.get('TO_EMAIL'),
        subject='Price Monitoring Alert',
         html_content=content
        )
    
    try:        
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


# if __name__ == "__main__":
#     send_email("<strong>Hi how are you?</strong>")

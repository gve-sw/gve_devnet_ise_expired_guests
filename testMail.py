from mail_service import Mail
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    #Get the log file
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
    d1 = Previous_Date.strftime("%d/%m/%Y")
    d1=d1.replace("/", "-")
    logs_path= f'./logs/{d1}.txt'

    mail_service = Mail(os.environ['EMAIL_SENDER'], os.environ['EMAIL_APP_PASSWORD'])
    mail_service.send_mail(os.environ['RECEIVER_EMAIL'], attachment=logs_path)
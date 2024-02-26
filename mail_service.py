# Copyright (c) 2023 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

class Mail():

    def __init__(self, sender_email, sender_password):
        
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_mail(self, receiver_email, attachment=False):


        sender = self.sender_email
        # Create message container 
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "ISE Deleted Users Logs"
        msg['From'] = sender
        msg['To'] = receiver_email

        if attachment:
            with open(attachment, "rb") as fil:
                part3 = MIMEApplication(
                    fil.read(),
                    Name=basename(attachment)
                )
            part3['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
            msg.attach(part3)
        

        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login(sender, self.sender_password)
        mail.sendmail(sender,receiver_email, msg.as_string())
        mail.quit()
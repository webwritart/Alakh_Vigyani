import time
from datetime import datetime
from extensions import Message, mail
from time import sleep
from urllib.parse import quote
import os
from flask import flash

sender_mail = os.environ.get('MAIL_USERNAME')

def send_email(subject, recipients, reply_mail, body, html, image_dict):
    message = Message(subject, sender=("ALAKH VIGYANI", sender_mail), recipients=recipients, reply_to=reply_mail)
    message.body = body
    if html:
        message.html = html
        root_path = '../static/images'
        if image_dict:
            for n in range(len(image_dict['file'])):
                file_format = 'image/' + image_dict['file'][n].split('.')[-1]
                message.attach(image_dict['file'][n], file_format,
                               open(os.path.join(root_path, image_dict['path'][n], image_dict['file'][n]), 'rb').read(),
                               'inline')
                # headers=[['content-ID', '<' + image_dict['file'][n].split('.')[0] + '>'], ])
    mail.send(message)
    print("Mail sent")







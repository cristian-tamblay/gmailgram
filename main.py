import imaplib
import email
import time
from client_secrets import client_id, client_password, bot_token, bot_chatID 
from email.header import make_header, decode_header
import requests
from bs4 import BeautifulSoup

def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def mail_handler(mail, mail_id):
    result, data = mail.fetch(str(mail_id), '(RFC822)')
    mail.store(str(mail_id), '+FLAGS', '(\Seen)')
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_subject = msg['subject']
            email_from = msg['from']
            email_from = 'From : '+str(make_header(decode_header(email_from)))
            if 'Google' in email_from:
                return # No quiero el spam de google :)
            email_subject = 'Subject : ' + str(make_header(decode_header(email_subject)))
            if msg.is_multipart():
                aux = ''
                for payload in msg.get_payload():
                    # if payload.is_multipart(): ...
                    body = payload.get_payload(decode=True)
                    try:
                        body = body.decode('utf-8').replace('#','').replace('*','')
                    except:
                        body = 'Picture'
                        # TODO Handle pictures
                    aux += body + '\n'
                    break
                body = aux
            else:
                body = msg.get_payload(decode=True)
                try:
                    body = body.decode('utf-8')
                except:
                    body = ''
            raw = BeautifulSoup(body, features="html.parser")
            message_to_send = (email_from+'\n'+email_subject+'\n\n'+raw.text)[:4096]
            print(message_to_send)
            print(telegram_bot_sendtext(message_to_send))


def read_email_from_gmail():
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(client_id,client_password)
        mail.select('inbox')

        result, data = mail.search(None, '(UNSEEN)')
        mail_ids = data[0]

        id_list = mail_ids.split()
        if len(id_list) == 0:
            return
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        if first_email_id == latest_email_id:
            mail_handler(mail, first_email_id)
        else:
            for i in range(latest_email_id,first_email_id, -1):
                mail_handler(mail, i)
        mail.logout() # Log out. Still connected.
# nothing to print here
while(True):
    read_email_from_gmail()
    time.sleep(15)

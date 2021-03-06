import imaplib
import email
import time
from client_secrets import client_id, client_password, bot_token, bot_chatID 
from email.header import make_header, decode_header
import requests 

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
            email_subject = 'Subject : ' + email_subject
            if msg.is_multipart():
                for payload in msg.get_payload():
                    # if payload.is_multipart(): ...
                    body = payload.get_payload(decode=True)
                    body = body.decode('utf-8')
                    break
            else:
                body = msg.get_payload(decode=True)
                body = body.decode('utf-8')
            telegram_bot_sendtext(email_from+'%0A'+email_subject+'%0A'+body)


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
    time.sleep(60)

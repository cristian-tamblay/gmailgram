import imaplib
import email
import time
from client_secrets import client_id, client_password
from email.header import make_header, decode_header

def read_email_from_gmail():
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(client_id,client_password)
        mail.select('inbox')

        result, data = mail.search(None, '(UNSEEN)')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            # need str(i)
            result, data = mail.fetch(str(i), '(RFC822)')
            mail.store(str(i), '+FLAGS', '(\Seen)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : '+str(make_header(decode_header(email_from))))
                    print('Subject : ' + email_subject)
                    if msg.is_multipart():
                        for payload in msg.get_payload():
                            # if payload.is_multipart(): ...
                            body = payload.get_payload(decode=True)
                            body = body.decode('utf-8')
                            print(body)
                    else:
                        body = msg.get_payload(decode=True)
                        body = body.decode('utf-8')
                        print(body)
# nothing to print here
while(True):
    print("Reading mail...")
    read_email_from_gmail()
    time.sleep(15)

"""
IMAP query reference https://www.skytale.net/blog/archives/23-Manual-IMAP.html
https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
https://coderwall.com/p/gorteg/python-s-imaplib
https://gist.github.com/robulouski/7441883
"""

import email
import email.header
import imaplib
import time
import csv
import re

from credentials import username, password, server_url

WAIT_TIME = 5

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(username, password) # login to mail account
mail.list()
mail.select("inbox") # connect to inbox.


# result, data = mail.uid('search', None, "ALL") # search and return uids instead
# latest_email_uid = data[0].split()[-1]
# result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
# raw_email = data[0][1]

email_store = {}
old_email_store = {}

while True:
    if old_email_store != email_store:
        old_email_store = email_store
        with open('monitor.csv', 'wt') as csvfile:
            csv_writer = csv.writer(csvfile)
            for key, items in email_store.items():
                csv_writer.writerow([key, items[0], items[1], items[2], items[3]])

    result, data = mail.search(None, "(FROM mailer-daemon@googlemail.com)")

    if result != 'OK':
        print("No messages found!")
        sys.exit(1)

    for num in data[0].split():
        status, data = mail.fetch(num, '(RFC822)')

        # How to fetch X-GM-MSGID
        # https://gist.github.com/davesteele/1323795
        ###########################################################################
        # response = mail.fetch(num, "(UID)" )[1][0]
        # uid = re.search("([0-9]+)\)", str(response)).group(1)
        # typ, msgdata = mail.uid( r'fetch', uid, r'(X-GM-MSGID)')
        # msgid_dec = re.search( r'X-GM-MSGID ([0-9]+)', str(msgdata[0]) ).group(1)
        # msgid_hex = hex(int(msgid_dec))
        ###########################################################################

        if status != 'OK':
            print("Error while getting message:", num)
            sys.exit(1)

        msg = email.message_from_bytes(data[0][1])
        raw_subject = email.header.make_header(email.header.decode_header(msg['Subject']))
        raw_date = email.header.make_header(email.header.decode_header(msg['Date']))
        raw_mid = email.header.make_header(email.header.decode_header(msg['Message-ID']))
        subject = str(raw_subject)
        date = str(raw_date)
        mid = str(raw_mid)
        email_content = msg.get_payload()[0].get_payload()[0].get_payload()[0].get_payload()
        mail_id = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', email_content)

        if mid in email_store.keys():
            continue
        else:
            email_store[mid] = [date, subject, mail_id.group(0), email_content]
    print("Done Looping")
    time.sleep(WAIT_TIME)

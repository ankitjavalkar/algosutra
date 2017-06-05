import sys
import smtplib
import csv

from credentials import username, password, server_url


class IncorrectValueError(Exception):
    pass


# Add Sender's email corresponding to the SMTP specified in credentials.py
FROM_ADDR = 'senders_email'

# Add subject line of email
SUB = 'subject_line'

# Add message body. No need to add salutations like Dear/Hello etc.
# MSG_BODY = ('Sample Message:'
#         'This mail has been sent by a Robot\n'
#         'that is going to take over the world\n'
#         '-----------\n'
#         'This script can now send a mail to anyone\n'
#         'you want from your email account'
#     )

MSG_BODY = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

def get_all_to_addr(csv_file):
    to_addr_list = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            email = row['email']
            to_addr_list.append((name.strip(), email.strip()))
    return to_addr_list


def set_message(from_addr, to_addr, subject, name, msg_body):
    if not from_addr:
        raise IncorrectValueError('The senders address is not provided')
    if not to_addr:
        raise IncorrectValueError('The recipients address is not provided')
    if not msg_body:
        raise IncorrectValueError('The message body is not provided')

    salutation = "Dear {0}".format(name)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(salutation+'\n'+msg_body, 'html')

    # msg = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}\n{4}""".format(from_addr,
    #     ", ".join(to_addr), subject, salutation, msg_body)
    return msg


def send_mail(from_addr, to_addr, subject, message):
    # The actual mail send
    try:
        server = smtplib.SMTP(server_url)
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(from_addr, to_addr, message.as_string())
        server.quit()
    except Exception as e:
        print e
        with open('errors.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([from_addr, to_addr[0], e.message])
        sys.exit(1)


def main():
    from_addr = FROM_ADDR
    subject = SUB
    msg_body = MSG_BODY
    csv_file = sys.argv[1]
    to_addr_list = get_all_to_addr(csv_file)
    for name, to_addr in to_addr_list:
        message = set_message(from_addr, [to_addr], subject, name, msg_body)
        send_mail(from_addr, [to_addr], subject, message)

if __name__ == '__main__':
    main()

import imaplib
import email
from getpass import getpass
import sys
#import pickle  
#from vectorize import vectorizer

host = 'imap.gmail.com'
username = input('Write your email : ')
password = getpass('Your password : ')

#Login to the account
mail = imaplib.IMAP4_SSL(host)
mail.login(username, password)
mail.select("inbox")

# GET THE LAST ID FOR THE FIRST TIME  
_, search_data = mail.search(None, 'UNSEEN') 
message_ids = list()

for num in search_data[0].split():
    message_ids.append(num)

try:
    last_id = message_ids[-1]
except Exception : 
    print('All emails are readed')
    sys.exit(0)


def fetchDecode(message_id, connection):
    """ A function to fetch an email given its id, decode it and printing it """

    result, data = connection.fetch(message_id, "(RFC822)")
    raw_email = data[0][1]

    #decoding the message
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    for part in email_message.walk():
        try:
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                plain_message = body.decode('utf-8')
                return plain_message
            else:
                continue

        except Exception:
            print('Error while decoding the message')
            break 

def checkNew(connection):
    """ A function to check if there are new emails """
    #Check if there are new emails
    connection.select("inbox")
    _, search_data = connection.search(None, 'UNSEEN') 
    message_ids = list() 
    for num in search_data[0].split():
        message_ids.append(num) 

    try:
        current_id = message_ids[-1]
        return current_id

    except IndexError:
        return 1

    
#Fetch for the first time the last message
email_message = fetchDecode(last_id, mail)

#Keep track of new emails and display get notified if there are new emails
while True:

    current_id = checkNew(mail)
    if current_id == 1:
        continue 

    elif current_id != 1:
        last_id = current_id 
        email_message = fetchDecode(last_id, mail)
        

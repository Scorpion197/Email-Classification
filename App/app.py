import imaplib
import email
from getpass import getpass
import sys
import pickle  
from vectorize import vectorizer

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


def fetch_decode(message_id, connection):
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

def check_new(connection):
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

def classify(email_message, vectClass):
    """ A function which returns whether an email is a spam or not  """ 
    message = list(email_message)
    vectorized_email = vectClass.transform(message)
    
    #Load the trained model from a file 
    try:
        models = pickle.load(open('trained_models', 'rb'))
        prediction = models[0].predict(vectorized_email)
        
    except FileNotFoundError:
        print("Model's file not found. Please save the model and try again ")
        sys.exit(0)
    
    prediction = list(prediction)
    number_zeros = prediction.count(0)
    number_ones = prediction. count(1)
    
    if number_zeros > number_ones:
        return 0 
    else:
        return 1

#Fetch for the first time the last message
email_message = fetch_decode(last_id, mail)

print(classify(email_message, vectorizer))

#Keep track of new emails and get notified if there are new non-spam emails
while True:

    current_id = check_new(mail)
    if current_id == 1:
        continue 

    elif current_id != 1:
        last_id = current_id 
        email_message = fetch_decode(last_id, mail)
        prediction = classify(email_message, vectorizer)

        if prediction == 1:
            continue 
        else:

            try:
                app = QApplication(sys.argv)
                window = NoteGui(email_message)  
                app.exec_()
                
            except KeyboardInterrupt:
                sys.exit(0)

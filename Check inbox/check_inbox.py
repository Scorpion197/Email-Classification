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
    
def classify(email_message, vectClass):
    """ A function which returns whether an email is a spam or not  """ 
    email_message = list(email_message)
    vectorized_email = vectClass.transform(email_message)
    models = pickle.load(open('trained_models', 'rb'))
    prediction = models[0].predict(vectorized_email)
    
    #Prediction is a list of 0 and 1 like the following one 
    """[0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0] """
    
    #turn the predictions into a list to count the number of zeros and the number of ones 
    # if the result is 1 ===> The email is a spam 
    #if the result is 0 ===> The email is not a spam 
    prediction = list(prediction) 
    number_zeros = prediction.count(0)
    number_ones = prediction. count(1)
    
    if number_zeros > number_ones:
        return 0 
    else:
        return 1

    
#Fetch for the first time the last message
email_message = fetchDecode(last_id, mail)
#print(classify(email_message, vectorizer))

#Keep track of new emails and display get notified if there are new emails
while True:

    current_id = checkNew(mail)
    if current_id == 1:
        continue 

    elif current_id != 1:
        last_id = current_id 
        email_message = fetchDecode(last_id, mail)
        
        #print(classify(email_message, vectorizer))


    

   
        

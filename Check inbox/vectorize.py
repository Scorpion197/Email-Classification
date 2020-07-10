import pandas as pd 
import numpy as np 
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer

import warnings 
warnings.filterwarnings('ignore')

df = pd.read_csv('emails.csv')
#Remove duplicates
df.drop_duplicates(inplace = True)

df = df.sample(frac=1).reset_index(drop=True)

def process_text(text):
    
    #1 Remove Punctuation
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    #2 Remove Stop Words
    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    
    #3 Return a list of clean words
    return clean_words

vectorizer = CountVectorizer(analyzer=process_text)
emails = vectorizer.fit_transform(df['text'])
""" I have done a copy of the notebook a python file so can import some variables from other scripts """

import pandas as pd 
import numpy as np 
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import confusion_matrix 
import matplotlib.pyplot as plt 
import seaborn as sns
import pickle

import warnings 
warnings.filterwarnings('ignore')

df = pd.read_csv('emails.csv')
#Remove duplicates
df.drop_duplicates(inplace = True)

df = df.sample(frac=1).reset_index(drop=True)

def process_text(text):
    
    #1 Remove Punctuationa
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    #2 Remove Stop Words
    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    
    #3 Return a list of clean words
    return clean_words

vectorizer = CountVectorizer(analyzer=process_text)
emails = vectorizer.fit_transform(df['text'])
X_train, X_test, y_train, y_test = train_test_split(emails, df['spam'], test_size = 0.20, random_state = 0)

models = {'Log':LogisticRegression(), 'Multi':MultinomialNB(),'Forest':RandomForestClassifier(n_estimators=30, criterion='gini', max_features = 10000, random_state =0)}

trained_models = list() 

for model in models.values():
    model.fit(X_train, y_train)
    acc = cross_val_score(model, X_train, y_train, scoring='accuracy', cv=10)
    print(acc.mean())
    trained_models.append(model)

#Choosing logistic regression after trying it on test data and saving it
pickle.dump(trained_models, open('trained_model', 'wb'))


loaded_model = pickle.load('trained_model', 'rb')
result = loaded_model.score(X_test, y_test)
print(result)

import random
import json
import pickle
import numpy as np


import nltk
from nltk.stem import WordNetLemmatizer


from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout
from keras.optimizers import SGD


lemmaitizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters=['?','.','...','()']

for intent in intents['intents']:
    for patterns in intents['patterns']:
        word_list = nltk.word_tokenize(patterns)
        words.extend(word_list)
        documents.append((word_list,intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])
words = [lemmaitizer.lemmatize(word)for word in words if word not in ignore_letters]  
words = sorted(set(words))   

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training = []
outoput_empaty =[0]*len(classes)
for document in documents:
    bag = []
    word_pattenrs = document[0]
    word_pattenrs = [lemmaitizer.lemmatize(word.lower())for word in word_pattenrs]
    for word in words:
      bag.append(1) if word in word_pattenrs else bag.append(0)
    ouput_row = list(outoput_empaty)
    ouput_row[classes.index(document[1])] = 1
    training.append([bag, ouput_row])
random.shuffle(training)    
training = np.array(training)
print(training )
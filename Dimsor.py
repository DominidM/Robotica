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

nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters=['?','.','...','()']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
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

try:

    train_x = []
    train_y = []
    
    for item in training:
        if len(item) == 2:
            train_x.append(item[0])  
            train_y.append(item[1])  
    
  
    training_x = np.array(train_x)
    training_y = np.array(train_y)
    
    print(f"Training X shape: {training_x.shape}")
    print(f"Training Y shape: {training_y.shape}")
    
       
except Exception as e:
    print(f"Error en Solución 1: {e}")
    print("Intentando Solución 2...")
    
    vectors = []
    labels = []
    
    for item in training:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            vectors.append(item[0])
            labels.append(item[1])
    
    
    if vectors:
        max_len_x = max(len(v) for v in vectors)
        max_len_y = max(len(l) for l in labels)
        
        
        vectors_padded = []
        labels_padded = []
        
        for v in vectors:
            if len(v) < max_len_x:
                v_padded = list(v) + [0] * (max_len_x - len(v))
            else:
                v_padded = list(v)[:max_len_x]
            vectors_padded.append(v_padded)
        
        for l in labels:
            if len(l) < max_len_y:
                l_padded = list(l) + [0] * (max_len_y - len(l))
            else:
                l_padded = list(l)[:max_len_y]
            labels_padded.append(l_padded)
        
        training_x = np.array(vectors_padded)
        training_y = np.array(labels_padded)
        
        print(f"Training X shape (padded): {training_x.shape}")
        print(f"Training Y shape (padded): {training_y.shape}")
    
    else:
        print("No se pudieron extraer vectores válidos")
        
        training_x = np.array([[0, 0, 0, 0]])
        training_y = np.array([[0, 0]])
        print("Usando datos dummy - revisa tu código de preparación de datos")

print(training)

train_x = [item[0] for item in training]
train_y = [item[1] for item in training]

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(learning_rate=0.001,decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer= sgd,metrics=['accuracy'])
train_process = model.fit(np.array(train_x),np.array(train_y), epochs=100, batch_size=5,verbose=1)
model.save("chatbot_model.h5",train_process)
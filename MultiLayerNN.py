import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.regularizers import l2
import tensorflow as tf

def init(x_train,y_train,x_test,y_test):#ftiaxnoume tous neurwnes 
    model = Sequential()
    model.add(Dense(4*28, input_dim=28, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4*28,#kernel_regularizer=l2(0.0001),
     activation='relu'))#,activity_regularizer=l2(0.01)
    model.add(Dense(2*28,activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    model.fit(x_train, y_train,batch_size=512, nb_epoch=1000, verbose=2,validation_data=(x_test, y_test))
    num_r=0
    num_w=0
    predictions=model.predict(x_test).round()#bazoume ola ta predictions se enan pinaka
    for i,j in enumerate(predictions):#emfanizoume ta swsta kai ta lathh
        if((y_test[i]==j).all()):
            num_r+=1
        else:
            num_w+=1
        
    print('Wrongs are: '+str(num_w))
    print('Rights are: '+str(num_r))
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import os

import createModel

#useDataset: https://www.kaggle.com/shayanfazeli/heartbeat

#to setup environments
baseDatasetPath = "../dataset/"
baseModelPath = "./models/"
baseCheckPointPath = baseModelPath + "checkPoints/"
batchSize = 128

#to use gpu efficient
#os.environ["CUDA_VISIBLE_DEVICES"]="2"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_visible_devices(gpus[2], 'GPU')
    tf.config.experimental.set_memory_growth(gpus[2], True)
  except RuntimeError as e:
    # 프로그램 시작시에 메모리 증가가 설정되어야만 합니다
    print(e)


normalData = pd.read_csv(baseDatasetPath + "ptbdb_normal.csv")
print(normalData)
abnormalData = pd.read_csv(baseDatasetPath + "ptbdb_abnormal.csv")

normalData = np.array(normalData)
abnormalData = np.array(abnormalData)

print("normalData:", normalData.shape, "\n", normalData)
print("abnormalData:",abnormalData.shape, "\n", abnormalData)



#data sampling.
#trainData = normalData(3000) + abnormalData(3000) = 6000
#testData = normalData(1000) + abnormalData(1000) = 2000
trainNumbers = 3000
testNumbers = 1000

xTrain = np.concatenate((normalData[:trainNumbers,:], abnormalData[:trainNumbers,:]),0)
yTrain = np.concatenate((np.zeros(trainNumbers,),np.ones(trainNumbers,)),0) #normal = 0, abnormal = 1
xTest = np.concatenate((normalData[trainNumbers:trainNumbers+testNumbers,:], abnormalData[trainNumbers:trainNumbers+testNumbers,:]),0)
yTest = np.concatenate((np.zeros(testNumbers,), np.ones(testNumbers,)),0)

print("xTrain.shape: ", xTrain.shape,"yTrain.shape: ", yTrain.shape)
print("xTest.shape: ", xTest.shape,"yTest.shape: ", yTest.shape)



#Converts a class vector (integers) to binary class matrix.
#to make output numbers 2
#because to match output matrix
from tensorflow.keras.utils import to_categorical
yTest = to_categorical(yTest)
yTrain = to_categorical(yTrain)
xTrain = np.expand_dims(xTrain, -1)
xTest = np.expand_dims(xTest, -1)

#print(yTest)



#deepLearning model
'''
from tensorflow.keras import Sequential
from tensorflow.keras import layers
from tensorflow.keras import optimizers

def create_model():
  model = Sequential()
  model.add(layers.Conv1D(filters=16, kernel_size=3, input_shape=(xTrain.shape[1], 1), activation='relu'))
  model.add(layers.Conv1D(filters=16, kernel_size=3, activation='relu'))
  model.add(layers.MaxPooling1D(pool_size = 3, strides=2))
  model.add(layers.Conv1D(filters=32, kernel_size=3, input_shape=(xTrain.shape[1],1), activation='relu'))
  model.add(layers.Conv1D(filters=32, kernel_size=3, activation='relu'))
  model.add(layers.MaxPooling1D(pool_size=3, strides=2))
  model.add(layers.LSTM(16))
  model.add(layers.Dense(units=2, activation="softmax"))
  model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adam(learning_rate=0.01), metrics=['accuracy'])

  return model
'''

'''
model = Sequential()
model.add(layers.Conv1D(filters=16, kernel_size=3, input_shape=(xTrain.shape[1], 1), activation='relu'))
model.add(layers.Conv1D(filters=16, kernel_size=3, activation='relu'))
model.add(layers.MaxPooling1D(pool_size = 3, strides=2))
model.add(layers.Conv1D(filters=32, kernel_size=3, input_shape=(xTrain.shape[1],1), activation='relu'))
model.add(layers.Conv1D(filters=32, kernel_size=3, activation='relu'))
model.add(layers.MaxPooling1D(pool_size=3, strides=2))
model.add(layers.LSTM(16))
model.add(layers.Dense(units=2, activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adam(learning_rate=0.01), metrics=['accuracy'])
'''

model = createModel.createModel(xTrain)

# use checkpoint to save models during train
#reference: https://www.tensorflow.org/tutorials/keras/save_and_load?hl=ko
checkpoint_path = baseCheckPointPath + "ecgTrainCheckPoint-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, verbose=1, save_weights_only=True, period=5)


model.save_weights(checkpoint_path.format(epoch=0))
model.fit(xTrain, yTrain, epochs = 50, batch_size=batchSize, validation_split=0.2, callbacks=[cp_callback])


loss, acc = model.evaluate(xTest, yTest, batch_size=batchSize, verbose=2)
#print("loss, acc = " , loss*100, acc*100)

o = model.predict(xTest)
print("model.predict(xTest): \n", o)

o = np.argmax(o,1) #output: 0 or 1
print("o: ", o)

yTest = np.argmax(yTest,1)
print("yTest accuracy : ", sum(np.equal(yTest,o))/len(yTest))


model.save(baseModelPath+'ecgTrainModel.h5')

import numpy as np
import pandas as pd
import tensorflow as tf
import os

#deepLearning model
from tensorflow.keras import Sequential
from tensorflow.keras import layers
from tensorflow.keras import optimizers

from performanceEvaluation import *
#import createModel #createModel.py

#to setup environments
"""gpuID = 2
baseDatasetPath = "../dataset/"
basePltSavePath = "./plots/"
baseModelPath = "./models/"
modelName="ecgTrainBasicModel.h5"
batchsize=128"""
gpuID = 2
baseDatasetPath = "../dataset/"
#basePltSavePath = "./plots/"
baseModelPath = "models"
modelName="ecgTrainBasicModel.h5"
batchsize=128

#to use gpu efficient
#os.environ["CUDA_VISIBLE_DEVICES"]="2"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_visible_devices(gpus[gpuID], 'GPU')
        tf.config.experimental.set_memory_growth(gpus[gpuID], True)
    except RuntimeError as e:
        # 프로그램 시작시에 메모리 증가가 설정되어야만 합니다
        print(e)
        
def main(file1,file2,selectModel,debugMode=False, eraseLastColumn=False,ensemble = False):
    loadModel = list()
    
    if ensemble: #model averaging ensemble
         
        modelForMIT = tf.keras.models.load_model("models/ecgTrainModel_MIT_dropout.h5")
        modelForPTB = tf.keras.models.load_model("models/ecgTrainModel_ptb_dropout.h5")
        #loadModel = VotingClassifier(estimators = [('model1', modelForMIT), ('model2', modelForPTB)], voting = 'soft') #hard: most Pick, soft: use probablity, and highest score is output.  ##VotingCalssifier needs models.fit
        loadModel.append(modelForMIT)
        loadModel.append(modelForPTB)
        
    else:
        loadModel = selectModel
        
    data, label = loadData(file1,file2, debugMode, eraseLastColumn)

    from tensorflow.keras.utils import to_categorical
    data = np.expand_dims(data,-1)

    if ensemble:
        if debugMode:
            label = to_categorical(label)
            prediction_debugresults = performanceEvaluationForEnsemble(data,label,loadModel)
            return prediction_debugresults
        else:
            predicts = np.array([model.predict(data) for model in loadModel])
            predictsScore = np.mean(predicts,axis=0)
            predicts = np.argmax(np.sum(predicts,axis=0),axis=1)
            results = []
            normal_result = []
            abnormal_result = []
            normalCount =0
            abnormalCount = 0
            #print(predicts)
            #print("!!!WARNING: predict Result are calculated by mean models predicts score because this model use essemble in this case!!!")
            for i in range (data.shape[0]):
                #print(data[0])
                result_str = "data {}: predict result: {}, predict: {}%".format( i + 1, predictResult(predicts[i]), np.max(predictsScore[i] * 100))
                if predicts[i]==0:
                    normalCount = normalCount+1
                    normal_result.append(result_str)
                else:
                    abnormalCount = abnormalCount+1
                    abnormal_result.append(result_str)
                results.append(result_str)
                
            return results, normalCount, abnormalCount, normal_result, abnormal_result
            
    else:

        loadModel = selectModel
        if debugMode:
            label = to_categorical(label)
            #test_loss,test_acc = loadModel.evaluate(data,label,batch_size=batchsize,verbose=2)
            
            #to calculate performance Evaluation
            prediction_debugresults = performanceEvaluation(data,label,loadModel)
            return prediction_debugresults
        else:
            predictions=loadModel.predict(data)

            predicted_classes = np.argmax(predictions, axis=1)
            #print(predict_result)
            results = []
            normal_result = []
            abnormal_result = []
            normalCount =0
            abnormalCount = 0
            for i, predicted_class in enumerate(predicted_classes):
                result_str = "data {}: predict result: {}, predict: {}%".format(
                    i + 1, predictResult(predicted_class), predictions[i, predicted_class] * 100
                )
    
                if predicted_class==0:
                    normalCount = normalCount+1
                    normal_result.append(result_str)
                else:
                    abnormalCount = abnormalCount+1
                    abnormal_result.append(result_str)
                results.append(result_str)
            return results, normalCount, abnormalCount, normal_result, abnormal_result
  
def predictResult(predictClass):
    if predictClass == 0:
        return "normal"
    else:
        return" abnormal"

    
def loadData(data1, file2="",debugMode=False, eraseLastColumn=False):
    #data1 = ""
    if file2 != "" and debugMode:
        #data1 = pd.read_csv(file1,header=None)
        #data1 = np.array(data1)
        #print(data1.shape[1])
        label1 = np.split(data1,data1.shape[1],axis=1)[data1.shape[1]-1]
        data1 = np.delete(data1,data1.shape[1]-1,1)
        
        data2 = pd.read_csv(file2,header=None)
        data2 = np.array(data2)
        label2 = np.split(data2,data2.shape[1],axis=1)[data2.shape[1]-1]
        data2 = np.delete(data2,data2.shape[1]-1,1)

        data = np.concatenate((data1,data2),0)
        label = np.concatenate((label1,label2),0)

        #print("data: ",data,"label: ", label)

        return data, label

    elif file2 != "":
        #data1 = pd.read_csv(file1,header=None)
        #data1 = np.array(data1)
        data1 = data1
        #print(data1.shape[1])
        #label1 = np.split(data1,data1.shape[1],axis=1)[data1.shape[1]-1]
        #data1 = np.delete(data1,data1.shape[1]-1,1)
        
        data2 = pd.read_csv(file2,header=None)
        data2 = np.array(data2)
        #label2 = np.split(data2,data2.shape[1],axis=1)[data2.shape[1]-1]
        #data2 = np.delete(data2,data2.shape[1]-1,1)
        if eraseLastColumn:
            data1 = np.delete(data1,data1.shape[1]-1,1)
            data2 = np.delete(data2,data2.shape[1]-1,1)

        data = np.concatenate((data1,data2),0)
        #label = np.concatenate((label1,label2),0)

        #print("data: ",data,"label: ", label)

        label = ""
        return data, label

    
    elif debugMode==True:
        #data = pd.read_csv(file1,header=None)
        #data = np.array(data)
        data = data1
        label = np.split(data,data.shape[1],axis=1)[data.shape[1]-1] 
        label[(label > 0)]=1
        print(label)
        
        data = np.delete(data,data.shape[1]-1,1) 

        return data,label

        
    else:
        #data = pd.read_csv(file1,header=None)
        #data = np.array(data)
        data=data1
        if eraseLastColumn:
            data = np.delete(data,data.shape[1]-1,1)

        label = ""

        return data, label
            

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file1", dest="file1", action="store")
    parser.add_argument("--file2", dest="file2", action="store",default="")

    parser.add_argument("-d", "--debugMode", dest="debugMode", action="store", default=False, help="True: to calculate performanceEvaluation with new dataset, False: only predict about new data" )
    parser.add_argument("-e", "--eraseLastColumn", dest="eraseLastColumn", action="store",default=False, help="True: erase Last Column in data, False: not erase Last Column in data")
    
    
    args = parser.parse_args()
        
    main(args.file1, args.file2, args.debugMode, args.eraseLastColumn)
    #loadData("../dataset/ptbdb_abnormal.csv","../dataset/ptbdb_normal.csv")
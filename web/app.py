import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request,send_file, Response,redirect, url_for,session
from werkzeug.utils import secure_filename
import pandas as pd
import os
from keras.models import load_model
from tensorflow import keras
import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
import io
import uuid
from ecgTest import *
from performanceEvaluation import *
from tensorflow.keras.utils import to_categorical

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'graph_img'
app.secret_key = 'some_secret_key'

model1 = keras.models.load_model('models/ecgTrainBasicModel.h5')
model2 = keras.models.load_model('models/ecgTrainDropoutModel.h5')
model3 = keras.models.load_model('models/ecgTrainTransformer.h5')

@app.route('/')
def upload():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/selectmodel')
def select_model():
    return render_template('selectmodel.html')

def create_graph(csv_graph, row):
    x = csv_graph.iloc[row]
    plt.figure()
    plt.plot(x)
    plt.axis([0, 188, 0, 1.2])
    if not os.path.exists(app.config['STATIC_FOLDER']):
        os.makedirs(app.config['STATIC_FOLDER'])

    graph_file_path = os.path.join(app.config['STATIC_FOLDER'], str(uuid.uuid4()) + '.png')
    plt.savefig(graph_file_path)
    plt.close()

    return graph_file_path

@app.route('/graphupload', methods=['GET', 'POST'])
def graphupload():
    return render_template('graphfileupload.html')

@app.route('/datagraph', methods=['GET', 'POST'])
def datagraph():
    data_num = int(request.form['result'])
    return render_template('datagraph.html',data_num=data_num)
    


@app.route('/graphresult', methods=['GET', 'POST'])
def graphresult():
    try:
        if request.method == 'POST':
            file = request.files['csvfile']
            csv_graph = pd.read_csv(file, header=None)
            row_count = len(csv_graph)
            row_options = [{'value': i, 'label': f'Row {i}'} for i in range(row_count)]
            row = int(request.form['row'])
            graph_file_path = create_graph(csv_graph, row)
            session['graph_file_path'] = graph_file_path
            return redirect(url_for('graphresult'))
        else:
            graph_file_path = session.get('graph_file_path', None)
            if graph_file_path:
                graph_filename = os.path.basename(graph_file_path)
                return render_template('graphresult.html', graph_filename=graph_filename)
            else:
                file = request.files['csvfile']
                data = pd.read_csv(file, header=None)
                row_count = len(data)
                row_options = [{'value': i, 'label': f'Row {i}'} for i in range(row_count)]
                row = int(request.form['row'])
                graph_file_path = create_graph(data, row)
                session['graph_file_path'] = graph_file_path
                graph_filename = os.path.basename(graph_file_path)
                return render_template('graphresult.html', graph_filename=graph_filename)
    except Exception as e:
        return render_template('error.html', error_message=str(e))    

@app.route('/get_graph')
def get_graph():
    graph_file_path = session.get('graph_file_path', None)
    if graph_file_path:
        return send_file(graph_file_path, mimetype='image/png', as_attachment=True)
    else:
        return 'Error: Graph file not found'
    

@app.route('/model1')
def model1_upload():
    return render_template('model1.html')

@app.route('/model1/result',methods=['GET','POST'])
def model1_result():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                prediction_results =main(data, file2, model2,False, True,False)
            else: 
                prediction_results=main(data,file2,model2,False,False,False)
            prediction_results1 = prediction_results[0]
            normal_count = prediction_results[1]
            abnormal_count = prediction_results[2]
            normal_result = prediction_results[3]
            abnormal_result = prediction_results[4]
            total_count = len(prediction_results1)    
            return render_template('model2_result.html',prediction_results=prediction_results1,normal_count= normal_count, abnormal_count=abnormal_count,normal_result=normal_result,abnormal_result=abnormal_result,total_count=total_count)
    except Exception as e:
        return render_template('error.html', error_message=str(e))     
        

@app.route('/model1/debugresult',methods=['GET','POST'])
def model1_debugresult():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 =main(data, file2, model1,True, True,False)
                return render_template('model1_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)
            else: 
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2=main(data,file2,mode1,True,False,False)
                return render_template('model1_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)    
    except Exception as e:
        return render_template('error.html', error_message=str(e))   
    
@app.route('/model2')
def model2_upload():
    return render_template('model2.html')  
 
@app.route('/model2/result',methods=['GET','POST'])
def model2_result():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                prediction_results =main(data, file2, model2,False, True,False)
            else: 
                prediction_results=main(data,file2,model2,False,False,False)
            prediction_results1 = prediction_results[0]
            normal_count = prediction_results[1]
            abnormal_count = prediction_results[2]
            normal_result = prediction_results[3]
            abnormal_result = prediction_results[4]
            total_count = len(prediction_results1)    
            return render_template('model2_result.html',prediction_results=prediction_results1,normal_count= normal_count, abnormal_count=abnormal_count,normal_result=normal_result,abnormal_result=abnormal_result,total_count=total_count)     
    except Exception as e:
        return render_template('error.html', error_message=str(e))   
@app.route('/model2/debugresult',methods=['GET','POST'])
def model2_debugresult():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 =main(data, file2, model1,True, True,False)
                return render_template('model2_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)
            else: 
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2=main(data,file2,mode1,True,False,False)
                return render_template('model2_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)    
    except Exception as e:
        return render_template('error.html', error_message=str(e))   
@app.route('/model3')
def model3_upload():
    return render_template('model3.html')  
 
@app.route('/model3/result',methods=['GET','POST'])
def model3_result():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                prediction_results =main(data, file2, model3,False, True,False)
            else: 
                prediction_results=main(data,file2,model3,False,False,False)
            prediction_results1 = prediction_results[0]
            normal_count = prediction_results[1]
            abnormal_count = prediction_results[2]
            normal_result = prediction_results[3]
            abnormal_result = prediction_results[4]
            total_count = len(prediction_results1)    
            return render_template('model3_result.html',prediction_results=prediction_results1,normal_count= normal_count, abnormal_count=abnormal_count,normal_result=normal_result,abnormal_result=abnormal_result,total_count=total_count)
    except Exception as e:
        return render_template('error.html', error_message=str(e))       
     
@app.route('/model3/debugresult',methods=['GET','POST'])
def model3_debugresult():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 =main(data, file2, model1,True, True,False)
                return render_template('model3_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)
            else: 
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2=main(data,file2,mode1,True,False,False)
                return render_template('model3_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)
    except Exception as e:
        return render_template('error.html', error_message=str(e))       
        
        
@app.route('/model4')
def model4_upload():
    return render_template('model4.html')  
 
@app.route('/model4/result',methods=['GET','POST'])
def model4_result():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            if data.shape[1] !=187:
                prediction_results =main(data, file2, model1,False, True,True)
            else: 
                prediction_results=main(data,file2,model1,False,False,True)
            prediction_results1 = prediction_results[0]
            normal_count = prediction_results[1]
            abnormal_count = prediction_results[2]
            normal_result = prediction_results[3]
            abnormal_result = prediction_results[4]
            total_count = len(prediction_results1)    
            return render_template('model4_result.html',prediction_results=prediction_results1,normal_count= normal_count, abnormal_count=abnormal_count,normal_result=normal_result,abnormal_result=abnormal_result,total_count=total_count)
    except Exception as e:
        return render_template('error.html', error_message=str(e))        
               
     
@app.route('/model4/debugresult',methods=['GET','POST'])
def model4_debugresult():
    try:
        if request.method == 'POST':
            f = request.files['csvfile']
            file2=""
            data = pd.read_csv(f,header=None)
            data = np.array(data)
            model1 = keras.models.load_model('models/ecgTrainBasicModel.h5')
            if data.shape[1] !=187:
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 =main(data, file2, model1,True, True,True)
                return render_template('model4_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)
            else: 
                accuracy, precision, recall, f1, kappa = 0, 0, 0, 0, 0
                auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2 = "", "","","",""
                accuracy, precision, recall, f1, kappa, auc, matrix_str1_1,matrix_str1_2,matrix_str2_1,matrix_str2_2=main(data,file2,model1,True,False,True)
                return render_template('model4_debugresult.html', accuracy=accuracy, precision=precision, recall=recall, f1=f1, kappa=kappa, auc=auc, matrix_str1_1=matrix_str1_1,matrix_str1_2=matrix_str1_2,matrix_str2_1=matrix_str2_1,matrix_str2_2=matrix_str2_2)
    except Exception as e:
        return render_template('error.html', error_message=str(e))           

          
@app.route('/performance')
def per_page():
    return render_template('performance_train.html')
@app.route('/performance_test')
def per_test():
    return render_template('performance_test.html')
@app.route('/performance_ptb')
def per_ptb():
    return render_template('performance_ptb.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')


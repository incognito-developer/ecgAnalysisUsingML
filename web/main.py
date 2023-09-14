import numpy as np
import pandas as pd
import argparse
import sys
sys.path.insert(0, '../models/')
import os
# os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
import utils
from models.ED import ED_Model

import config
import warnings
import tensorflow as tf
import click

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.6  
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

warnings.filterwarnings("ignore")



def run_flask_command():
    Model = "ED"
    Kmin = 1
    Kmax = 50
    Queries = 20
    Tasks = 20
    Retrain = 0
    BatchSize = 32
    MaxEpochs = 100
    OutputDir = "../weights/"
    Verbose = 0

    result = project(Model, Kmin, Kmax, Queries, Tasks, Retrain, BatchSize, MaxEpochs, OutputDir, Verbose)
    return result
    
def project(Model, Kmin, Kmax, Queries, Tasks, Retrain, BatchSize, MaxEpochs, OutputDir, Verbose):
    X_test, y_test = utils.load_test_data()
    #print('Loaded test data, running tasks for ED...\n')
    ED_model = ED_Model()
    result = ED_model.print_metrics_ED(X_test, y_test, k_min=Kmin, k_max=Kmax, num_tasks=Tasks, q=Queries)
    return result    

if __name__ == "__main__": 
    main()


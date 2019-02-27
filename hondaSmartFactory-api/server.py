# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:29:27 2019

@author: Puneet Samnani 724538
"""

"""Filename: server.py
"""

import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def apicall():
    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """
    try:
        test_json = request.get_json()
        test = pd.read_json(test_json, orient='records')


        # Getting the protRecord_IDs separated out
        prot_ids = test['protRecord_ID'].values
        
        # pull those 6 variables here    
        X_test = test[['phaStd','weldTimeActualValue','resistanceActualValue','stabilisationFactorActValue','uipActualValue' ,'uirExpulsionTime']].values

    except Exception as e:
        raise e

    clf = 'finalRf.model'

    if test.empty:
        return(bad_request())
    else:
        #Load the saved model
        print("Loading the model...")
        loaded_model = None
        with open('./'+clf,'rb') as f:
            loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")
        
        predictions = loaded_model.predict(X_test)

        """Add the predictions as Series to a new pandas dataframe
                                OR
           Depending on the use-case, the entire test data appended with the new files
        """
        prediction_series = list(pd.Series(predictions))

        final_predictions = pd.DataFrame(list(zip(prot_ids, prediction_series)), columns = ['protRecord_Id', 'y_Pred-Rf'])

        """We can be as creative in sending the responses.
           But we need to send the response codes as well.
        """
        responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        responses.status_code = 200

        return (responses)
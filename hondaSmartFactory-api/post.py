# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 16:45:10 2019

@author: Puneet Samnani 724538
"""

#  waitress-serve --listen=*:8000 server:app


import json
import requests
import pandas as pd
"""Setting the headers to send and accept json responses
"""
header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}

"""Reading test batch
"""
df = pd.read_excel('sampleTest.xlsx',sheet_name = 'Sheet1')
df = df.head()

"""Converting Pandas Dataframe to json
"""

dfs = df[['protRecord_ID','phaStd','weldTimeActualValue','resistanceActualValue','stabilisationFactorActValue','uipActualValue' ,'uirExpulsionTime']]

data = dfs.to_json(orient='records')
data



"""POST <url>/predict
"""
resp = requests.post("http://view-localhost:8000/predict", \
                    data = json.dumps(data),\
                    headers= header)
resp.status_code

"""The final response we get is as follows:
"""
resp.json()

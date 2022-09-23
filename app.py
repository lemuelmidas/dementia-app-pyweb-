from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
#from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.exceptions import SessionClosedException
import pandas as pd
import pickle
import warnings
import argparse

#app= Flask(__name__)

warnings.filterwarnings("ignore")



with open('model_xgb.pkl', 'rb') as f:
    model= pickle.load(f)

with open('columns.pkl', 'rb') as f:
    model_columns= pickle.load(f)
    
def prediction(prediction_df):
    model = pickle.load(open('model_xgb.pkl', 'rb'))
    query= pd.DataFrame(prediction_df, index= [0])
    result=list(model.predict(query))
    final_result= round(result[0],3)
    
    return final_result

def values():
    #input_group("Dementia Prediction")
    put_markdown(
    
    '''
    Dementia Prediction Web App
    '''
    , lstrip=True
    )
    
    model_inputs= input_group(
    "Dementia Prediction",
    [
        select("Visit", name='visit', options= [('One', 1), ('Two', 2), ('Three', 3), ('Four', 4), ('Five', 5)]),
        input("MR Delay", name= 'mr_delay', type= FLOAT),
        radio("What's your gender?", name='gender', options= [('Male', 1), ('Female', 0)]),
        input("Your Age", name= 'age', type= FLOAT),
        input("EDUC", name= 'educ', type= FLOAT),
        select("SES", name='ses', options= [('One', 1), ('Two', 2), ('Three', 3), ('Four', 4)]),
        input("MMSE", name= 'mmse', type= FLOAT),
        input("eTIV", name= 'etiv', type= FLOAT),
        input("nWBV", name= 'nwbv', type= FLOAT),
        input("ASF", name= 'asf', type= FLOAT),
        select("CDR", name='cdr', options= [('None', 0), ('Half', 0.5), ('One', 1), ('Two', 2)]),
    ])
    
    
    prediction_df= pd.DataFrame(data= [[model_inputs[i] for i in ['visit', 'mr_delay', 'gender', 'age', 'educ','ses', 'mmse', 'cdr', 'etiv','nwbv','asf']]],
                               columns= ['Visit', 'MR Delay', 'M/F', 'Age', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV', 'nWBV','ASF'])
    
    DementiaCategory= prediction(prediction_df)
    #prediction_text=''
    if DementiaCategory<=0:
        put_markdown("You are converted")
    
    elif DementiaCategory<=1:
        put_markdown("You are at high risk of dementia")
    
    else:
        put_markdown("You are at very low risk of dementia")
    
    
#app.add_url_rule('/tool', 'webio_view', webio_view(values), methods=['GET', 'POST','OPTIONS'])
    
    
if __name__== '__main__':
  parser= argparse.ArgumentParser()
  parser.add_argument("-p", "--port", type= int, default= 8080)
  args= parser.parse_args()
        
  start_server(values, port= args.port)
    
        
  
    
        
        
    
#if __name__== "__main__":
#    try:
#        values()
#    except SessionClosedException:
#        print("The session was closed unexpectedly")
    
    
        
        
    
        
        
        
        

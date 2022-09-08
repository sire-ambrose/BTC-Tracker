import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
import yfinance as yf



def get_array(df):
    arr= np.zeros((1, 60))

    feat= np.zeros((1, 60))

    for row in range(df.shape[0]):
        price= df.iloc[row, 0]
        column= df.iloc[row, 1]
        feat[0, column]= price
        if column== 59:
            arr= np.concatenate((arr, feat), axis=0)
            feat= np.zeros((1, 60))
    return arr[1:, :]


def get_x(df):
    df['time']= pd.to_datetime(df.time)
    df['minutes']= pd.to_datetime(df.time).dt.minute
    df['date']= pd.to_datetime(df.time).dt.date
    df['hour']= pd.to_datetime(df.time).dt.hour
    high= df[['date', 'hour', 'High']].groupby(['date', 'hour'], as_index=False).max()['High'].values.reshape(-1, 1)
    low= df[['date', 'hour', 'Low']].groupby(['date', 'hour'], as_index=False).min()['Low'].values.reshape(-1, 1)
    #hour= df[['date', 'hour', 'minutes']].groupby(['date', 'hour'], as_index=False).min()['hour'].values.reshape(-1, 1)/100


    arr= get_array(df[['Close', 'minutes']])
    arr= np.concatenate((arr, high[:arr.shape[0], :], low[:arr.shape[0], :]), axis=1)
    

    columns= [str(i) for i in range(60)]
    columns.extend(['high', 'low'])
    arr_df= pd.DataFrame(arr, columns= columns)
    arr_df['open']= arr_df['59'].shift(1)
    arr_df.dropna(axis=0, inplace=True)

    arr_df['high-low']= arr_df['high']-arr_df['low']
    arr_df['high-59']= arr_df['high']-arr_df['59']
    arr_df['high-open']= arr_df['high']-arr_df['open']

    arr_df['open-59']= arr_df['open']-arr_df['59']
    arr_df['open-low']= arr_df['open']-arr_df['low']

    arr_df['59-low']= arr_df['59']-arr_df['low']
    return arr_df



def get_current():    
    #timezone = pytz.timezone("UTC")
    now= datetime.now()+timedelta(hours=1)
    now= datetime.fromtimestamp(now.timestamp())
    year= now.year
    month= now.month
    day= now.day
    hour= now.hour
    minute= now.minute
    # set time zone to UTC

    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    end = datetime(year, month, day, hour, 0, 0)#+timedelta(hours=1)

    start= datetime(year, month, day, hour, 59, 0)- timedelta(hours=3)

    rates = yf.download('BTC-USD', end=end, start=start, interval='1m')
    rates['time']= rates.index
    return rates

def prob():
    cv_results={}
    cv_results["estimator"]=[joblib.load('model0.pkl'), joblib.load('model1.pkl'), joblib.load('model2.pkl'), joblib.load('model3.pkl'), joblib.load('model4.pkl')]
    test_x=get_x(get_current())

    result=pd.DataFrame()
    c=0
    for algorithms in cv_results['estimator']:
        result[str(c)]= algorithms.predict_proba(test_x)[:, 1]
        c+=1
    bull= round(result.median(axis=1).values[0]*100, 2)

    result=pd.DataFrame()
    c=0
    for algorithms in cv_results['estimator']:
        result[str(c)]= algorithms.predict_proba(test_x)[:, 0]
        c+=1
    bear= round(result.median(axis=1).values[0]*100, 2)

    return 'Bullish: '+str(bull)+'%\nBearish: '+str(bear)+ '%'
print(prob())

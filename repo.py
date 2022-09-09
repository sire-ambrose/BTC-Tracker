import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
import yfinance as yf



def get_array(df):
    arr= np.zeros((1, 60))

    feat= np.zeros((1, 60))
    for day in df.date.unique():
        day_df= df[df['date']==day]
        for hour in day_df.hour.unique():
            hour_df= day_df[day_df['hour']==hour]
            for row in range(hour_df.shape[0]):
                price= hour_df.iloc[row, 0]
                column= hour_df.iloc[row, 1]
                feat[0, column]= price
            arr= np.concatenate((arr, feat), axis=0)
            feat= np.zeros((1, 60))
    return arr[1:, :]


def get_x(df):
    df= df.rename({'Open':'open', 'Close':'close', 'High':'high', 'Low':'low'}, axis=1)
    df['time']= pd.to_datetime(df.time)
    df['minutes']= pd.to_datetime(df.time).dt.minute
    df['date']= pd.to_datetime(df.time).dt.date
    df['hour']= pd.to_datetime(df.time).dt.hour

    open= df[['date', 'hour', 'open']].groupby(['date', 'hour'],  as_index= False).nth([0])
    open=open['open'].values.reshape(-1,1)


    high= df[['date', 'hour', 'high']].groupby(['date', 'hour'], as_index=False).max()['high'].values.reshape(-1, 1)
    low= df[['date', 'hour', 'low']].groupby(['date', 'hour'], as_index=False).min()['low'].values.reshape(-1, 1)

    close= df[['date', 'hour', 'close']].groupby(['date', 'hour'],  as_index= False).nth([-1])
    close=close['close'].values.reshape(-1,1)

    
    arr= get_array(df[['close', 'minutes', 'date', 'hour']])
    foward_dff=np.diff(arr, n=1)

    for i in range(2, arr.shape[1]):
        foward_dff= np.concatenate( (foward_dff, np.diff(arr, n=i) ), axis=1 )

    arr= np.concatenate((arr, open[:arr.shape[0], :], high[:arr.shape[0], :], low[:arr.shape[0], :], close[:arr.shape[0], :]), axis=1)


    columns= ['min_'+str(i) for i in range(60)]

    columns.extend(['open', 'high', 'low', 'close'])
    arr_df= pd.DataFrame(arr, columns= columns)
    arr_df= pd.concat([pd.DataFrame(foward_dff), arr_df], axis=1)
    arr_df.dropna(axis=0, inplace=True)

    arr_df['high-low']= arr_df['high']-arr_df['low']
    arr_df['high-close']= arr_df['high']-arr_df['close']
    arr_df['high-open']= arr_df['high']-arr_df['open']

    arr_df['open-close']= arr_df['open']-arr_df['close']
    arr_df['open-low']= arr_df['open']-arr_df['low']

    arr_df['close-low']= arr_df['close']-arr_df['low']
    columns= [str(i) for i in range(60)]
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
    cv_results["estimator"]=[joblib.load('model0.pkl'), joblib.load('model1.pkl'), joblib.load('model2.pkl')]
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

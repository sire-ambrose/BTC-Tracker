import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from repo import prob
st.write("# Stock Analysis")
'\n'

name_dict={'BTC':'BTC-USD'}

def display(name):
    st.write("### "+name)
    
    '\n'

    period = st.selectbox('Period',['1 day', '5 days', '1 month', '3 months', '6 months', '1 year', '2 years'],key=name+'period')

    'You selected: ', period 
    period_dict={'1 day':'1d', '5 days':'5d', '1 month':'1mo', '3 months':'3mo', '6 months':'6mo', '1 year':'1y', '2 years':'2y'}
    '\n'
    
    interval= st.selectbox('Interval', [ '1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'])
    data=yf.download(tickers='BTC', period=period_dict[period], interval = interval)
    
    #st.write(data)

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    

    fig.show()
    st.plotly_chart(fig)
    '\n'
    st.write(prob())

display(name_dict['BTC'])

st.write('\n\n\n\n\n\n')
st.write('### Contact Developer : ')
st.write('[Facebook](https://www.facebook.com/profile.php?id=100005064735483)')
st.write('[Github ](https://github.com/sire-ambrose)')
st.write('[Linkedin](https://www.linkedin.com/in/ambrose-ikpele-61643419a)')

import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
st.write("# Stock Analysis")
'\n'

name_dict={'BTC':'BTC-USDT', 'Facebook':'FB'}

def display(name):
    st.write("### "+name)
    
    '\n'

    period = st.selectbox('Period',['1 day', '5 days', '1 month', '3 months', '6 months', '1 year', '2 years'],key=name+'period')

    'You selected: ', period 
    period_dict={'1 day':'1d', '5 days':'5d', '1 month':'1mo', '3 months':'3mo', '6 months':'6mo', '1 year':'1y', '2 years':'2y'}
    '\n'
    data=yf.download(tickers=name_dict[name], period=period_dict[period], interval = '15m')
    
    st.write(data)

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    

    fig.show()
    st.plotly_chart(fig)

 
for i in name_dict:
    display(i)
    ''

st.write('\n\n\n\n\n\n')
st.write('### Contact Developer : ')
st.write('[Facebook](https://www.facebook.com/profile.php?id=100005064735483)')
st.write('[Github ](https://github.com/sire-ambrose)')
st.write('[Linkedin](https://www.linkedin.com/in/ambrose-ikpele-61643419a)')

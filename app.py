import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import random
import pandas as pd

# App title
st.set_page_config(page_title="Stockly", layout="wide")

st.sidebar.title("Stockly")

st.sidebar.markdown('---')
st.markdown('''
# Stockly: A Stock Market Analysis App By InSight3D
Shown are the stock price data for query companies!

- App built by [Neil Shah](https://neilshahdev.tk) &  [InSight3D](http://insight3d.tech)
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
''')
st.write('---')



# Sidebar
st.sidebar.subheader('Select Search Date')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())
st.sidebar.markdown('---')

# Retrieving tickers data
st.sidebar.subheader('Select Company')

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
second_table = payload[1]

df = first_table

symbols = df['Symbol'].values.tolist()

text_box = st.sidebar.text_input("Stock Ticker", value="AAPL", max_chars=5, help="Enter The Companies Ticker", placeholder = random.choice(symbol))
# ticker_list_raw = pd.read_excel('https://github.com/NeilShah2026/stockly/blob/main/company_list.xlsx')
# ticker_list = ticker_list_raw['Symbol'].values.tolist()
# tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list, index=40) # Select ticker symbol

tickerData = yf.Ticker(text_box) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

# Ticker data
st.header('**Ticker Data**')
st.write(tickerDf)

# Break
st.write('---')

# Live Data
st.header('**Live Data**')
live_info = tickerData.info['regularMarketPrice']
market_cap = tickerData.info['marketCap']
volume = tickerData.info['regularMarketVolume']
st.write('**Current price: %s**' % live_info)
st.write('**Market Cap: %s**' % market_cap)
st.write('**Volume: %s**' % volume)

# Break
st.write('---')

# Past Month Data
monthbefore = end_date - datetime.timedelta(days=30)
st.header('**Past Month**')
past_month = tickerData.history(period='1d', start=monthbefore, end=end_date)
st.write(past_month)
d1 = cf.QuantFig(past_month, title=f'{tickerDf} Past Month', legend='top', name='GS')
d1.add_bollinger_bands()
fig = d1.iplot(asFigure=True)
st.plotly_chart(fig)

# Break
st.write('---')

# Past Year
yearbefore = end_date - datetime.timedelta(days=365)
st.header('**Past Year**')
past_year = tickerData.history(perdiod='1d', start = yearbefore, end = end_date)
st.write(past_year)
d2 = cf.QuantFig(past_year, title=f'{tickerDf} Past Year', legend='top', name='GS')
d2.add_bollinger_bands()
fig_write = d2.iplot(asFigure=True)
st.plotly_chart(fig_write)

# Break
st.write('---')

# Bollinger bands
st.header('**Query Chart**')
st.write(tickerDf)
qf=cf.QuantFig(tickerDf,title=f'{text_box} Query Chart',legend='top',name='GS')
qf.add_bollinger_bands()
fig2 = qf.iplot(asFigure=True)
st.plotly_chart(fig2)

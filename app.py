import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from yahoo_fin import stock_info as si
import datetime
import urllib.request
from PIL import Image

st.markdown("<h1 style='text-align: center; color: blue;'>S&P 500 APP</h1>", unsafe_allow_html=True)
imag = Image.open('main.jpg')
st.image(imag, use_column_width=True)
# Web scraping of S&P 500 data
#
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

@st.cache
def get_todays_rate(data):
    df = {}
    lst = []
    for x in data.Symbol:
        try:
            df[x] = round(si.get_live_price(x),2)
        except:
            data.drop(data[data.Symbol == x].index)

    return df,data

def create_main_page(today_rate):
    # st.markdown("""
    # This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
    # """)
    st.sidebar.header("Today's Stock Price")
    cols1,cols2 = st.sidebar.beta_columns(2)
    cols1.subheader("Name")
    cols2.subheader("Price")
    for x in today_rate:
        cols1.write(x)
        cols2.write(today_rate[x]) 

def web_plot(data):

    fig, axs = plt.subplots(6, figsize=(20,16))
    index = 0
    for x in data.columns:
        axs[index].plot(data.index, data[x], color='red', alpha = 0.8)
        # axs[index].xticks(rotation=90)
        # plt.title(symbol, fontweight='bold')
        axs[index].set_xlabel('Date', fontweight='bold')
        axs[index].set_ylabel(x, fontweight='bold')
        index += 1
    st.pyplot(plt)


@st.cache
def get_info(name,s,e):
    data = yf.download(name, start = s, end = e)
    info_df = yf.Ticker(name.upper()).info
    return data,info_df

def show_info(name, s, e):

    data,info_df = get_info(name,s,e)
    if info_df['logo_url'] != None:
        urllib.request.urlretrieve(info_df['logo_url'], "local-filename.jpg")
        img = Image.open('local-filename.jpg')
        st.image(img)
    st.title(info_df['shortName'] + '(' + name+ ') information')
    st.write(info_df['longBusinessSummary'])
    col1, col2 = st.beta_columns(2)
    for x in info_df:
        if info_df[x] == None or x == 'longBusinessSummary':
            continue
        col1.write(x)
        col2.write(info_df[x])
    # st.write(data.columns)
    web_plot(data)


df = load_data()
# df = shuffle(df)
df = df[:100]
today_rate,df = get_todays_rate(df)
create_main_page(today_rate)

with st.beta_expander('For Specific Company'):
    selected_company = None
    start_date = None
    end_date = None
    st.header('User Input Features')
    st.subheader("""Enter the Name of the Company""")
    selected_company = st.text_input('')
    st.subheader("""Or select from drop down box""")
    selected_company = st.selectbox('',df.Symbol)
    st.subheader("""Enter start year yyyy/mm/dd""")
    start_date = st.date_input('', datetime.date(12, 11, 12))
    st.subheader("""Enter End year yyyy/mm/dd""")
    end_date = st.date_input('', datetime.date(12, 12, 12))

if st.button('Search'):
    show_info(selected_company, start_date, end_date)


import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Oh Snap! Card Rules"
)

# CSS to inject contained in a string
hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """
        
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# css to remove the top padding
remove_padding = '''
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>

'''

st.markdown(remove_padding,unsafe_allow_html=True)

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

st.title("Oh Snap! Card Rules")

type = sorted(list(df['Type'].drop_duplicates()))
type_choice = st.radio('Filter on a card type', type, horizontal=True)
df = df[df['Type'] == type_choice]
card = sorted(list(df['Card'].drop_duplicates()))
card_choice = st.selectbox('Filter on a card', card)
df = df[df['Card'] == card_choice]
df = df.drop(['Type', 'Card', 'Description'], axis=1)
st.table(df)
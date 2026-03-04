
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Indian Credit Card Intelligence", layout="wide")
st.title("Bank-Grade Credit Card Analytics - India")

try:
    df = pd.read_csv("Credit card transactions - India - Simple.csv")
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    df['City'] = df['City'].str.replace(', India','').str.strip()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Overview", "Fraud Map", "Predictions"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spend", f"₹{df['Amount'].sum()/1e7:.1f} Cr")
    c2.metric("Transactions", f"{len(df):,}")
    c3.metric("Avg Transaction", f"₹{df['Amount'].mean():,.0f}")
    st.plotly_chart(px.line(df.groupby('Date')['Amount'].sum().reset_index(), x='Date', y='Amount'))

with tab2:
    try:
        with open("india_credit_map.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=600)
    except Exception as e:
        st.warning(f"Could not load map: {e}")

with tab3:
    st.write("High-value & at-risk customers ready for action")

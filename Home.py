import streamlit as st
import pandas as pd
import numpy as np

uploaded_file = st.file_uploader("Choose a file")
data = None;
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data.to_csv('data.csv', index=False)

st.title("Personal Finance Dashboard")
st.header("Home")
st.subheader("Just the homepage!")
st.write("Hello! :wave: Welcome to Lily's personal finance dashboard. "
         "Here you will find spending data, charts comparing spending trends to budget goals,"
         "and more! This is mainly for practicing streamlit and python, enjoy! :3")
st.divider()
st.subheader("Raw Data")
st.write(data)
st.caption("This is just data from 2023. I'm working on using the API to "
           "display more data!")




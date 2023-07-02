import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

st.header("See Income")
st.subheader("See how much you've made! (That sounds weird but you get it)")
st.write("Here's where you can see how much money has been added to the savings account!")
data = None;
file_upload = st.file_uploader("Go to Intuit Mint and upload the CSV file of your transactions!")
timeframe = st.radio("See income for the past: ", ('Week', 'Month', 'Year'))

st.divider()
thirtyone = ['04', '06', '09', '11']
thirty = ['01', '03', '05', '07', '08', '10', '12']

from datetime import datetime


def findDuration(dataset, length):
    thirtyone = ['04', '06', '09', '11']
    thirty = ['01', '03', '05', '07', '08', '10', '12']

    count = 0
    today = datetime.now().date()  # Extract only the date component

    for i in range(len(dataset)):
        row = dataset.loc[i]
        row_date = datetime.strptime(row['Date'], '%m/%d/%Y').date()  # Convert the row date string to a date object

        if row_date.month == today.month:
            x = today.day - row_date.day
            days = x + 1  # Since you start from day 1
        else:
            toMonth = 0
            if row_date.month in thirtyone:
                toMonth = 31 - row_date.day
            elif row_date.month in thirty:
                toMonth = 30 - row_date.day
            else:
                # Handling February's case with leap year check
                is_leap_year = today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)
                toMonth = 29 if is_leap_year else 28 - row_date.day

            days = toMonth + today.day

        if days > length:
            break
        count += 1

    return count


charty = None

if file_upload is not None:
    data = pd.read_csv(file_upload)

    if timeframe == 'Week':
        charty = data.head(findDuration(data, 7))
    elif timeframe == 'Month':
        charty = data.head(findDuration(data, 30))
    elif timeframe == 'Year':
        charty = data.head(findDuration(data, 365))
    else:
        charty = data

    charty = charty[(charty['Account Name'] == 'YOUNG ADULT SAVINGS') & (charty['Category'] == 'Income')]

    charty2 = charty[['Date', 'Amount']]
    total = 0
    charty3 = pd.DataFrame(columns=['Date', 'Amount'])
    for index in range(len(charty2)-1, -1, -1):
        total += charty2.iloc[index]['Amount']
        datey = charty2.iloc[index]['Date']
        charty3.loc[index] = [datey, total]

    charty3['Date'] = pd.to_datetime(charty3['Date'])
    charty3['Date'] = charty3['Date'].dt.date
    charty3.set_index('Date', inplace=True)
    st.line_chart(charty3['Amount'])
    st.caption("This is a line chart representing the income you have made over "
               "the time frame you specified! I'm using only the savings account, since that's where I set up my income "
               "deposits for.")

    col3, col4 = st.columns(2)

    with col3:
        st.write(charty3)
        st.caption("This is just the raw data for the line chart. The line chart helps you see the trends and stuff, "
                   "while this is an easier way of seeing the numbers directly. Each amount is the amount made so far"
                   " + the amount in that deposit, so the bottom number is the total amount you've gained "
                   "over the specified timeframe. Double click the to see the full date or amount.")

    with col4:
        st.write(charty2)
        st.caption("This is a chart of how much was actually made per deposit in your "
                   "designated timeframe! This one does not add each one to the total, it's just the raw data."
                   " Double click to see the full date or amount.")


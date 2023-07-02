import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from packagex import findDuration

st.header("Budgeting!")
st.subheader("Make a budget and see how you're doing on it.")
st.write("Just write in what you want your budget for the week/month/year to be (how much you want to spend),"
         "and this page will calculate how much money you have left in your budget to spend for the duration of "
         "time selected!")
timeframe = st.radio("Pick a time frame: ", ("Week", "Month", "Year"))
file = st.file_uploader("Upload your CSV file from Intuit Mint here!")
budget = st.number_input("Input what you want your maximum spending to be for the duration you selected.")
data = None
charty = None



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


if file is not None:
    data = pd.read_csv(file)
    if timeframe == 'Week':
        charty = data.head(findDuration(data, 7))
    elif timeframe == 'Month':
        charty = data.head(findDuration(data, 30))
    elif timeframe == 'Year':
        charty = data.head(findDuration(data, 365))
    else:
        charty = data
    charty = charty[(charty['Account Name'] == 'CHECKING')]
    charty2 = charty[['Date', 'Amount']]
    total = 0
    charty3 = pd.DataFrame(columns=['Date', 'Amount'])
    for index in range(len(charty2) - 1, -1, -1):
        total += charty2.iloc[index]['Amount']
        datey = charty2.iloc[index]['Date']
        charty3.loc[index] = [datey, total]

    charty3['Date'] = pd.to_datetime(charty3['Date'])
    charty3['Date'] = charty3['Date'].dt.date
    charty3.set_index('Date', inplace=True)
    st.line_chart(charty3['Amount'])
    st.caption("This is a line chart representing what you've spent over "
               "the time frame you specified!")

    st.write(charty3.iloc[-1])
    if charty3.iloc[-1]['Amount'] - budget < 0:
        st.write("This is how much you've spent so far! Your budget is " + str(budget) + ", so you have $" +
                 str(round((budget - charty3.iloc[-1]['Amount']), 2))+ " left until you exceed your budget!")
    elif charty3.iloc[-1]['Amount'] - budget > 0:
        st.write("This is how much you've spent so far! You've exceeded your budget by $" + str(round((budget -
                 charty3.iloc[-1]['Amount']), 2)) + '.')
    else:
        st.write("You've hit your budget exactly, having spent $" + str(budget) + ".")

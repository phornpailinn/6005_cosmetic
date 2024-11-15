import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
from pinotdb import connect
import plotly.express as px

# Establish a connection to the Pinot server
conn = connect(host='54.169.176.13', port=8099, path='/query/sql', schema='http')

# Create a cursor object to execute the query for Topic7_HOPPING
curs = conn.cursor()
curs.execute('''
SELECT 
  ID, 
  SUM(USER_COUNT) AS totalUsers, 
  SUM(REGION_COUNT) AS totalRegions, 
  SUM(GENDER_COUNT) AS totalGenders
FROM Topic7_HOPPING
GROUP BY ID
ORDER BY totalUsers DESC;
''')
tables = [row for row in curs.fetchall()]
df_topic7 = pd.DataFrame(tables, columns=['ID', 'totalUsers', 'totalRegions', 'totalGenders'])

# Create a cursor object to execute the query for 2_users
curs.execute('''
SELECT 
  regionid, 
  gender, 
  COUNT(*) AS totalUsers
FROM 2_users
GROUP BY regionid, gender
ORDER BY totalUsers DESC;
''')
tables = [row for row in curs.fetchall()]
df_users = pd.DataFrame(tables, columns=['regionid', 'gender', 'totalUsers'])

# Create a cursor object to execute the query for 1_pageviews
curs.execute('''
SELECT 
  userid, 
  COUNT(*) AS totalPageviews
FROM 1_pageviews
GROUP BY userid
ORDER BY totalPageviews DESC;
''')
tables = [row for row in curs.fetchall()]
df_pageviews = pd.DataFrame(tables, columns=['userid', 'totalPageviews'])

# Streamlit layout: 2 columns and 2 rows
col1, col2 = st.columns(2)

# Display the bar plot in the first column
with col1:
    st.subheader('Total Users per ID (Topic7_HOPPING)')
    fig1 = px.bar(df_topic7, x='ID', y='totalUsers', 
                  title='Total Users per ID',
                  labels={'ID': 'ID', 'totalUsers': 'Total Users'},
                  color='totalUsers', text='totalUsers')
    st.plotly_chart(fig1)

# Display the pie chart in the second column
with col2:
    st.subheader('User Distribution by Gender per Region (2_users)')
    fig2 = px.pie(df_users, names='gender', values='totalUsers', 
                  title='User Distribution by Gender per Region',
                  color='gender', labels={'gender': 'Gender', 'totalUsers': 'Total Users'})
    st.plotly_chart(fig2)

# Display the tables in the second row, spanning both columns
col3, col4 = st.columns(2)

with col3:
    st.subheader('User Pageviews (1_pageviews)')
    st.dataframe(df_pageviews)

with col4:
    st.subheader('Total Users and Regions per ID (Topic7_HOPPING)')
    st.dataframe(df_topic7)


import pandas as pd
import plotly.express as px
import streamlit as st
from pinotdb import connect

# Function to fetch data from Pinot
def fetch_data(query):
    conn = connect(host='13.250.117.179', port=8099, path='/query/sql', schema='http')
    curs = conn.cursor()
    curs.execute(query)
    tables = [row for row in curs.fetchall()]
    return tables

# Query for User Distribution by Gender per Region
query_gender_region = '''
SELECT
  regionid,
  gender,
  COUNT(*) AS totalUsers
FROM 2_users
GROUP BY regionid, gender
ORDER BY totalUsers DESC;
'''

# Query for User Pageviews
query_pageviews_user = '''
SELECT
  userid,
  COUNT(*) AS totalPageviews
FROM 1_pageviews
GROUP BY userid
ORDER BY totalPageviews DESC;
'''

# Query for Regions with More Than 4 Users
query_regions = '''
SELECT regionid, COUNT(*) AS user_count
FROM 2_users
GROUP BY regionid
HAVING user_count > 4
ORDER BY user_count DESC;
'''

# Fetch data
gender_region_data = fetch_data(query_gender_region)
pageviews_user_data = fetch_data(query_pageviews_user)
regions_data = fetch_data(query_regions)

# Convert to DataFrame
df_gender_region = pd.DataFrame(gender_region_data, columns=['regionid', 'gender', 'totalUsers'])
df_pageviews_user = pd.DataFrame(pageviews_user_data, columns=['userid', 'totalPageviews'])
df_regions = pd.DataFrame(regions_data, columns=["regionid", "user_count"])

# Streamlit Layout: 2 Rows and 2 Columns
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# First chart: Pie chart - User Distribution by Gender per Region
with col1:
    fig1 = px.pie(df_gender_region, names='gender', values='totalUsers',
                  title='User Distribution by Gender per Region', color='gender')
    st.plotly_chart(fig1)

# Second chart: Bar chart - Total Pageviews per User
with col2:
    fig2 = px.bar(df_pageviews_user, x="userid", y="totalPageviews", title="Pageviews per User",
                  labels={"userid": "User ID", "totalPageviews": "Total Pageviews"},
                  color="totalPageviews", color_continuous_scale="Blues")
    st.plotly_chart(fig2)

# Third chart: Bar chart - Regions with More Than 4 Users
with col3:
    fig3 = px.bar(df_regions, x="regionid", y="user_count", title="Regions with More Than 4 Users",
                  labels={"regionid": "Region ID", "user_count": "User Count"})
    st.plotly_chart(fig3)

# Display the DataFrame of regions data in the fourth column
with col4:
    st.write("### Regions Data")
    st.dataframe(df_regions)



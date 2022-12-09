import streamlit as st
import pandas as pd
import numpy as np
import psycopg2

#acct connection
conn = psycopg2.connect(**st.secrets["postgres"])
cur = conn.cursor()

sql = """select distinct conditions.nct_id ,conditions.name,studies.last_known_status, studies.last_update_posted_date, facilities.country, facilities.city from conditions 
join studies
on studies.nct_id = conditions.nct_id
join facilities
on facilities.nct_id = studies.nct_id
where (conditions.name = 'Diabetes Mellitus, Type 2' and (studies.last_known_status = 'Recruiting' or studies.last_known_status = 'Active, not recruiting'))"""

cur.execute(sql)

records = cur.fetchall()

cur.close()
conn.close()

st.subheader('Clinical trials')

ids = []
for i in len(records):
  ids.append(records[i][0])

trials = st.selectbox('Please select clinical trial:',ids)

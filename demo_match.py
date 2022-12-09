import streamlit as st
import pandas as pd
import numpy as np
import psycopg2

#acct connection
conn = psycopg2.connect(**st.secrets["postgres"])
cur = conn.cursor()

all_con = """select distinct conditions.name from conditions"""

all_coun = """select distinct facilities.country from facilities"""

cur.execute(all_con)
records = cur.fetchall()
cur.close()

cur = conn.cursor()
cur.execute(all_coun)
countries_all = cur.fetchall()
cur.close()

st.subheader('Clinical trials')

ids = []
for i in range(len(records)):
  ids.append(records[i][0])
  
countries = []
for m in range(len(countries_all)):
  countries.append(countries_all[m][0])

condition = st.selectbox('Please select the condition you want to look for:',ids)

country = st.selectbox('Please select the location you want to attend the trial:',countries)

cur = conn.cursor()
sql = """select distinct conditions.nct_id ,conditions.name,studies.last_known_status, studies.last_update_posted_date, facilities.country, facilities.city from conditions 
join studies
on studies.nct_id = conditions.nct_id
join facilities
on facilities.nct_id = studies.nct_id
where (conditions.name = '{fcondition}' and facilities.country = '{fcountry}' and (studies.last_known_status = 'Recruiting' or studies.last_known_status = 'Active, not recruiting'))""".format(fcondition=str(condition),fcountry=str(country))
cur.execute(sql)
trials_ = cur.fetchall()
cur.close()

  
trials = []
for n in range(len(trials_)):
  trials.append(trials_[n][0])


conn.close()

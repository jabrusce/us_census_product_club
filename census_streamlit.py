import streamlit as st
import pickle
import numpy as np
import pandas as pd
# from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

#Headers
st.header('Product Club')
st.subheader("US Census")

#Choose Action
user_pop_total = st.number_input('Population Total?')
user_unemployment_rate = st.number_input('Unemployment Rate?')
user_income = st.number_input('Median Income?')
user_temp = st.number_input('Climate (Temperature in Farenheit)?')

city = st.checkbox('find a place')

if city:
    # user_pop_total = 500_000
    # user_unemployment_rate = 0.02
    # user_income = 80_000
    # user_temp = 70

    data = pd.read_csv('./data/df-income-climate.csv').drop(columns=['Unnamed: 0']).rename(columns={'Unnamed: 0.1': 'county'})
    scaler = StandardScaler() 

    cols = data.columns[1:]
    X_scaled = scaler.fit_transform(data[cols])
    
    kmeans = pickle.load(open('./model/kmeans.pkl', 'rb'))
    kmeans.fit(X_scaled)
    data['label'] = kmeans.labels_

    y = data.label
    knn = KNeighborsClassifier()
    knn.fit(X_scaled, y)

    pref={'pop_total': user_pop_total, 
        'unemployment_rate': user_unemployment_rate, 
        'income': user_income,
        'temp': user_temp}
    
    prefdf = pd.DataFrame.from_dict(pref, orient='index').T
    pref_scaled = scaler.transform(prefdf)
    pred = knn.predict(pref_scaled)[0]
    
    user_df = data[data.label == pred].county
    user_show = pd.DataFrame(user_df)
    user_show

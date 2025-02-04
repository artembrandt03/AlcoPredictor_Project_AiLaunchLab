# -*- coding: utf-8 -*-
"""Project Streamlit

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16my6wBWYhi-wczOAip4ABAI5X7-11xNb
"""

# installs streamlit in colab
#!pip install -q streamlit

# ----------------------------------------------------------------

#! pip install kaggle
#! mkdir student_alcohol_consumption_data

# fetches dataset from kaggle
#! kaggle datasets download uciml/student-alcohol-consumption

#! mv student-alcohol-consumption.zip student_alcohol_consumption_data
#! unzip student_alcohol_consumption_data/student-alcohol-consumption.zip -d student_alcohol_consumption_data

# Commented out IPython magic to ensure Python compatibility.
#%%writefile app.py
import streamlit as st
from streamlit.logger import get_logger

import pandas as pd
import seaborn as sns
import numpy as np
import math

import matplotlib.pyplot as plt

from scipy import stats
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


LOGGER = get_logger(__name__)


def run():
  st.set_page_config(
        page_title="Student Alcohol Consumption Classification",
        page_icon="📊",
    )

  st.title('Classification')

  st.subheader('Raw Data')

  # reads the CSV data into a DataFrame named 'df'
  df = pd.concat(
      [
      pd.read_csv('student-mat.csv'),
      pd.read_csv('student-por.csv')
      ],
      ignore_index=True)

  # displays the dataset
  st.write(df)

  st.link_button("Dataset Link",
          "https://www.kaggle.com/datasets/uciml/student-alcohol-consumption")

  # removes duplicate row(s) from dataset
  df.drop_duplicates(keep='first', inplace=True)

  st.write('### Display Numerical Plots')

  # Select box to choose which feature to plot
  feature_to_plot = st.selectbox('Select a numerical feature to plot', ['Medu',
  'Fedu', 'famrel', 'age', 'traveltime', 'studytime', 'freetime', 'goout',
  'Dalc', 'Walc', 'health', 'absences', 'failures', 'G1', 'G2', 'G3'])

  # Plot the selected feature
  if feature_to_plot:
    st.write(f'Distribution of {feature_to_plot}:')
    fig = plt.figure(figsize=(10, 6))
    plt.hist(df[feature_to_plot], bins=30, color='skyblue', edgecolor='black')
    plt.xlabel(feature_to_plot)
    plt.ylabel('Count')
    st.pyplot(fig)

  st.write('### Display Categorical Plots')

  # Select box to choose which feature to plot
  feature_to_plot = st.selectbox('Select a feature to plot', ['sex', 'address',
  'reason', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher',
  'internet', 'romantic'])

  # Plot the selected categorical feature
  if feature_to_plot:
    st.write(f'Distribution of {feature_to_plot}:')
    bar_chart = st.bar_chart(df[feature_to_plot].value_counts())

  # encodes columns
  df['sex_encode'] = LabelEncoder().fit_transform(df['sex'])
  df['address_encode'] = LabelEncoder().fit_transform(df['address'])
  df['famsize_encode'] = LabelEncoder().fit_transform(df['famsize'])
  df['Pstatus_encode'] = LabelEncoder().fit_transform(df['Pstatus'])
  df['Mjob_encode'] = LabelEncoder().fit_transform(df['Mjob'])
  df['Fjob_encode'] = LabelEncoder().fit_transform(df['Fjob'])
  df['reason_encode'] = LabelEncoder().fit_transform(df['reason'])
  df['guardian_encode'] = LabelEncoder().fit_transform(df['guardian'])
  df['schoolsup_encode'] = LabelEncoder().fit_transform(df['schoolsup'])
  df['famsup_encode'] = LabelEncoder().fit_transform(df['famsup'])
  df['paid_encode'] = LabelEncoder().fit_transform(df['paid'])
  df['activities_encode'] = LabelEncoder().fit_transform(df['activities'])
  df['nursery_encode'] = LabelEncoder().fit_transform(df['nursery'])
  df['higher_encode'] = LabelEncoder().fit_transform(df['higher'])
  df['internet_encode'] = LabelEncoder().fit_transform(df['internet'])
  df['romantic_encode'] = LabelEncoder().fit_transform(df['romantic'])

  # defines X (features) and y (target) and removes duplicate features
  X = df.drop(['school', 'Dalc', 'Walc', 'sex', 'address', 'famsize', 'Pstatus',
               'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup', 'famsup',
               'paid', 'activities', 'nursery', 'higher', 'internet',
               'romantic'], axis=1)
  y = df['Dalc']

  # splits the dataset into X_train, X_test, y_train, and y_test,
  # 10% of the data for testing
  X_train, X_test, y_train, y_test = \
                        train_test_split(X, y, test_size=0.1, random_state=0)

  # instantiates a model
  model = RandomForestClassifier(random_state=0)

  # trains the model
  model.fit(X_train, y_train)

  # creates Streamlit app
  st.write('## Predict Your Own Charges')

  # user input for features
  sex = st.selectbox('Sex', ['Male', 'Female'])
  age = st.slider('Age', min_value=15, max_value=22, value=15)
  address = st.selectbox('Address Type', ['Urban', 'Rural'])
  famsize = st.selectbox('Family Size',
   ['Less than or equal to 3', 'Greater than 3'])
  Pstatus = st.selectbox('Parent\'s Cohabition Status', ['Together', 'Apart'])
  Medu = st.selectbox('Mother\'s Education',
   ['None', 'Primary Education (4th Grade)', '5th to 9th Grade',
    'Secondary Education', 'Higher Education'])
  Fedu = st.selectbox('Father\'s Education',
   ['None', 'Primary Education (4th Grade)', '5th to 9th Grade',
    'Secondary Education', 'Higher Education'])
  Mjob = st.selectbox('Mother\'s Job',
   ['Teacher', 'Health', 'Services', 'At Home', 'Other'])
  Fjob = st.selectbox('Father\'s Job',
   ['Teacher', 'Health', 'Services', 'At Home', 'Other'])
  reason = st.selectbox('Reason to choose the school',
   ['Close to Home', 'School Reputation', 'Course Preference', 'Other'])
  guardian = st.selectbox('Guardian', ['Father', 'Mother', 'Other'])
  traveltime = st.selectbox('Home to School Travel Time',
   ['< 15 min', '15 - 30 min', '30 min - 1 hour', '> 1 hour'])
  studytime = st.selectbox('Weekly Study Time',
   ['< 2 hours', '2 - 5 hours', '5 - 10 hours', '> 10 hours'])
  failures = st.slider('Number of past class failures',
                       min_value=1, max_value=4, value=1)
  schoolsup = st.selectbox('Extra Educational Support', ['Yes', 'No'])
  famsup = st.selectbox('Family Educational Support', ['Yes', 'No'])
  paid = st.selectbox('Extra Paid Classes within the Course Subject',
   ['Yes', 'No'])
  activities = st.selectbox('Extra-Curricular Activities', ['Yes', 'No'])
  nursery = st.selectbox('Attended Nursery School', ['Yes', 'No'])
  higher = st.selectbox('Wants to Take Higher Education', ['Yes', 'No'])
  internet = st.selectbox('Internet Access at Home', ['Yes', 'No'])
  romantic = st.selectbox('with a Romantic Relationship', ['Yes', 'No'])
  famrel = st.selectbox('Quality of Family Relationships',
   ['Very Bad', 'Poor', 'Mediocre', 'Good', 'Excellent'])
  freetime = st.selectbox('Free Time after School',
   ['Very Low', 'Low', 'Moderate', 'High', 'Very High'])
  goout = st.selectbox('Going out with Friends',
   ['Very Low', 'Low', 'Moderate', 'High', 'Very High'])
  health = st.selectbox('Current Health Status',
   ['Very Bad', 'Bad', 'Neutral', 'Good', 'Very Good'])
  absences = st.slider('Number of School Absences', min_value=0, max_value=93,
                       value=0)
  G1 = st.slider('First Period Grade', min_value=0, max_value=20, value=0)
  G2 = st.slider('Second Period Grade', min_value=0, max_value=20, value=0)
  G3 = st.slider('Final Period Grade', min_value=0, max_value=20, value=0)

  sex_encode = 0 if sex == 'Female' else 1
  address_encode = 0 if address == 'Rural' else 1
  famsize_encode = 0 if famsize == 'Greater than 3' else 1
  Pstatus_encode = 0 if Pstatus == 'Apart' else 1

  Medu = 0 if Medu == 'None' \
  else 1 if Medu == 'Primary Education (4th Grade)' \
  else 2 if Medu == '5th to 9th Grade' \
  else 3 if Medu == 'Secondary Education' \
  else 4 if Medu == 'Higher Education' \
  else None

  Fedu = 0 if Fedu == 'None' \
  else 1 if Fedu == 'Primary Education (4th Grade)' \
  else 2 if Fedu == '5th to 9th Grade' \
  else 3 if Fedu == 'Secondary Education' \
  else 4 if Fedu == 'Higher Education' \
  else None

  Mjob_encode = 0 if Mjob == 'At Home' \
  else 1 if Mjob == 'Health' \
  else 2 if Mjob == 'Other' \
  else 3 if Mjob == 'Services' \
  else 4 if Mjob == 'Teacher' \
  else None

  Fjob_encode = 0 if Fjob == 'At Home' \
  else 1 if Fjob == 'Health' \
  else 2 if Fjob == 'Other' \
  else 3 if Fjob == 'Services' \
  else 4 if Fjob == 'Teacher' \
  else None

  reason_encode = 0 if reason == 'Course Preference' \
  else 1 if reason == 'Close to Home' \
  else 2 if reason == 'Other' \
  else 3 if reason == 'School Reputation' \
  else None

  guardian_encode = 0 if guardian == 'Father' \
  else 1 if guardian == 'Mother' \
  else 2 if guardian == 'Other' \
  else None

  traveltime = 1 if traveltime == '< 15 min' \
  else 2 if traveltime == '15 - 30 min' \
  else 3 if traveltime == '30 min - 1 hour' \
  else 4 if traveltime == '> 1 hour' \
  else None

  studytime = 1 if studytime == '< 2 hours' \
  else 2 if studytime == '2 - 5 hours' \
  else 3 if studytime == '5 - 10 hours' \
  else 4 if studytime == '> 10 hours' \
  else None

  schoolsup_encode = 0 if schoolsup == 'No' else 1
  famsup_encode = 0 if famsup == 'No' else 1
  paid_encode = 0 if paid == 'No' else 1
  activities_encode = 0 if activities == 'No' else 1
  nursery_encode = 0 if nursery == 'No' else 1
  higher_encode = 0 if higher == 'No' else 1
  internet_encode = 0 if internet == 'No' else 1
  romantic_encode = 0 if romantic == 'No' else 1

  famrel = 1 if famrel == 'Very Bad' \
  else 2 if famrel == 'Poor' \
  else 3 if famrel == 'Mediocre' \
  else 4 if famrel == 'Good' \
  else 5 if famrel == 'Excellent' \
  else None

  freetime = 1 if freetime == 'Very Low' \
  else 2 if freetime == 'Low' \
  else 3 if freetime == 'Moderate' \
  else 4 if freetime == 'High' \
  else 5 if freetime == 'Very High' \
  else None

  goout = 1 if goout == 'Very Low' \
  else 2 if goout == 'Low' \
  else 3 if goout == 'Moderate' \
  else 4 if goout == 'High' \
  else 5 if goout == 'Very High' \
  else None

  health = 1 if health == 'Very Bad' \
  else 2 if health == 'Bad' \
  else 3 if health == 'Neutral' \
  else 4 if health == 'Good' \
  else 5 if health == 'Very Good' \
  else None

  # predicts alcohol consumption
  prediction = model.predict([[age, Medu, Fedu, traveltime, studytime, failures,
  famrel, freetime, goout, health, absences, G1, G2, G3, sex_encode,
  address_encode, famsize_encode, Pstatus_encode, Mjob_encode, Fjob_encode,
  reason_encode, guardian_encode, schoolsup_encode, famsup_encode, paid_encode,
  activities_encode, nursery_encode, higher_encode, internet_encode,
                               romantic_encode]])

  # displays result
  st.write('Predicted Alcohol Consumption:', prediction)


if __name__ == "__main__":
    run()

#!npm install localtunnel

#!streamlit run /content/app.py &>/content/logs.txt &

import urllib
print("Password/Enpoint IP for localtunnel is:",urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n"))
#!npx localtunnel --port 8501
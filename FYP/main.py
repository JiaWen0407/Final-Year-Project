# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 20:48:25 2022

@author: Loo Jia Wen 0129868
"""

#Import modules
import streamlit as st
import hydralit as hy
import pandas as pd
import pyrebase
from CurrentUser import CurrentUser
from Pages.SignUpPage import SignUpPage
from Pages.LoginPage import LoginPage 
from Pages.StudentInformationPage import StudentInformationPage
from Pages.EditingStudentInformationPage import EditingStudentInformationPage
from Pages.EditingPasswordFaceRecognitionPage import EditingPasswordFaceRecognitionPage

# Firebase configuration
if 'config' not in st.session_state:
    # Firebase configurations key
    st.session_state.config = {
        "apiKey": "AIzaSyBApj8k7d9Lh44OdtNw80_U35s8rUYuQ8g",
        "authDomain": "student-information-syst-11111.firebaseapp.com",
        "databaseURL": "https://student-information-syst-11111-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "student-information-syst-11111",
        "storageBucket": "student-information-syst-11111.appspot.com",
        "messagingSenderId": "381311492781",
        "appId": "1:381311492781:web:bb314fc8203dad3cb45c24",
        "measurementId": "G-QKJBZLWZ6Y",
        "serviceAccount": "C:/Users/jiawe/Desktop/FYP/serviceAccountKey.json"
    }
    
    
# Firebase authentication
if 'firebase' not in st.session_state:
    st.session_state.firebase = pyrebase.initialize_app(st.session_state.config)
    
if 'firebase_storage' not in st.session_state:
    st.session_state.firebase_storage = pyrebase.initialize_app(st.session_state.config)

if "auth" not in st.session_state:
    st.session_state.auth = st.session_state.firebase.auth()
    
# Storage
if 'storage' not in st.session_state:
    st.session_state.storage = st.session_state.firebase_storage.storage()

# Database
if 'db' not in st.session_state:
    st.session_state.db = st.session_state.firebase.database()
       
# Load user data from firebase
if 'users_db' not in st.session_state:
    st.session_state.users_db = st.session_state.db.child("users").get()

# Users dataframe
if 'users' not in st.session_state:
    st.session_state.users = pd.DataFrame(columns = ['user_id', 'student_id', 'email', 'password', 'reg_date', 'del_date', 'login_time','student_name', 'ic_passport','country','marital_status','contact_number','home_address','update_date'])

# Current user
if 'current_user' not in st.session_state:
    st.session_state.current_user = CurrentUser()
    
# Load data into dataframe
if st.session_state.users_db.val() is not None:
    for u in st.session_state.users_db.each():
        st.session_state.users = st.session_state.users.append(u.val(), ignore_index=True)


if __name__ == '__main__':
    
    app = hy.HydraApp(title='Student Information System',
                      hide_streamlit_markers=True,
                      favicon="🏫")
    
    app.add_app('Sign Up', app=SignUpPage(), is_login=True, is_unsecure=True)
    app.add_app('Login', app=LoginPage(),  is_login=True)
    app.add_app('Student Information', icon="🏠", app=StudentInformationPage(),is_home=True)
    app.add_app('Edit', icon="✏️", app=EditingStudentInformationPage())
    app.add_app('Change Password & Face Recognition', icon="🔑", app=EditingPasswordFaceRecognitionPage())
    
    app.run()


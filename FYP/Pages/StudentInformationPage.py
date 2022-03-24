# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 20:54:52 2022

@author: Loo Jia Wen 0129868
"""

#Import modules
import streamlit as st
from hydralit import HydraHeadApp

class StudentInformationPage(HydraHeadApp): 
    def run(self):
        
        # Display user information        
        student_info = st.session_state.db.child("users").order_by_child("user_id").equal_to(st.session_state.current_user['user_id']).get()
        st.title('Student Information')        
    
        for s in student_info.each():
            # Display user last login history
            st.subheader("Last login: " + s.val()["login_time"])
            # Display Student Information
            st.write("Student ID: " + s.val()["student_id"] )
            st.write("Name: " + s.val()['student_name'])
            st.write("IC / Passport: " + s.val()['ic_passport'])  
            st.write("Country: " + s.val()['country'])
            st.write("Marital Status: " + s.val()['marital_status'])
            st.write("Email Address: " + s.val()['email'])
            st.write("Contact Number: " + s.val()['contact_number'])  
            st.write("Home Address: " + s.val()['home_address'])
            st.write("Last edited: " + s.val()['update_date'])
            
        print('\nLoaded Student Information from real-time database\n')   


# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 20:56:16 2022

@author: Loo Jia Wen 0129868
"""

#Import modules
import streamlit as st
from hydralit import HydraHeadApp
from datetime import datetime

class EditingStudentInformationPage(HydraHeadApp): 
    def run(self):
        
        print("\nDisplaying editing student information page...\n")
        st.title('Edit Student Information')
        # Display user information        
        student_info = st.session_state.db.child("users").order_by_child("user_id").equal_to(st.session_state.current_user['user_id']).get()     
    
        for s in student_info.each():
            # Display user last login history
            st.subheader("Last login: " + s.val()["login_time"])
        
            with st.form(key='student_information_form'):
                st.write("Student ID: " + s.val()['student_id'])
                student_name = st.text_input("Name: ", s.val()['student_name'])
                # date_of_birth = st.date_input("Date of Birth: ")
                ic_passport = st.text_input("IC / Passport: ", s.val()['ic_passport'])  
                country = st.selectbox("Country: ",
                          ['', 'Australia', 'Canada', 'China', 'Japan', 'Malaysia', 'USA'] )
                
                marital_status = st.radio("Marital Status: ",
                      ['Prefer not to say','Single', 'Married'])
        
                st.write("Email Address: " + st.session_state.current_user['email'])
                
                contact_number = st.text_input("Contact Number: ", s.val()['contact_number'])
                
                home_address = st.text_input("Home Address: ", s.val()['home_address'])
                
                btn_update = st.form_submit_button(label='UPDATE')
            
            
            if btn_update:
                now = datetime.now()
                update_date = now.strftime("%d/%m/%Y %H:%M:%S")
                                    
                u = {
                        
                        'student_name': student_name,
                        'ic_passport': ic_passport,
                        'country': country,
                        'marital_status': marital_status,
                        'contact_number': contact_number,
                        'home_address': home_address,
                        'update_date': update_date
                        }
                
                #Update data into real-time database
                st.session_state.db.child('users').child(st.session_state.current_user['user_id']).update(u)
                print("\n Student information updated successfully.\n")
                print(u)
                st.success("Updated successfully")
                

# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 20:51:04 2022

@author: Loo Jia Wen 0129868
"""

#Import modules
import streamlit as st
from hydralit import HydraHeadApp
from datetime import datetime
from validate_email import validate_email
#importing opencv from python
import cv2

class SignUpPage(HydraHeadApp):  
    
    def reset_checkbox(self):
        st.session_state.run = False            
    
    def run(self):
        
        st.title('Student Information System')
        
        col1, col2 = st.columns(2)
        
        with col1:
                     
            # Password Sign up form
            # Prevent page refresh after one input
            with st.form(key='password_signup_form'):
                st.header('Sign Up')
                student_id = st.text_input('Student ID: ', key='student_id')
                email = st.text_input('Email Address: ', key='email') 
                password  = st.text_input('Password: ', type="password", key='password')
                checkbox_next = st.checkbox('Confirm your password?', key='checkbox_next')
                btn_next = st.form_submit_button(label='NEXT')
        
            if btn_next:  
                
                now = datetime.now()
                reg_date = now.strftime("%d/%m/%Y %H:%M:%S")
                
                #check the user account is available
                if st.session_state.users.empty == True:
                      exists = False
                else:
                    exists = email in st.session_state.users.email
                    
                if not exists:
                    #check if the email is available
                    valid = validate_email(email)
                    
                    if valid:
                        #create a user with their email and password for signup
                        user = st.session_state.auth.create_user_with_email_and_password(email, password)
                        
                        u = {
                            'user_id': user['localId'],
                            'student_id': student_id,
                            'email': email,
                            'password': password,
                            'reg_date': reg_date,
                            'del_date': None,
                            'login_time': '-',
                            'student_name': '-',
                            'ic_passport': '-',
                            'country': '-',
                            'marital_status': '-',
                            'contact_number': '-',
                            'home_address': '-',
                            'update_date': '-'
                            }
                        
                        #save user account (data) into real-time database
                        st.session_state.db.child('users').child(user['localId']).set(u)
                        #save it to the dataframe
                        st.session_state.users= st.session_state.users.append(u, ignore_index=True)
                        print("\nUser data added to the real time database.\n")
                        print(u)
                        print("\n")
                    
                    else:
                       st.error('Incorrect email address.')
                   
                else:
                    st.warning('This account is already registered.')
                    
          
                if student_id == "" and email != "" and password != "" and btn_next:
                    st.warning('Please enter your student id.')
                    
                elif student_id == "" and email == "" and password != "" and btn_next:
                    st.warning('Please enter your student id and email address.')
                    
                elif student_id == "" and email != "" and password == "" and btn_next:
                    st.warning('Please enter your student id and password.')
                    
                elif email == "" and student_id != "" and password != "" and btn_next:
                    st.warning('Please enter your email address.')
                    
                elif email == "" and student_id != "" and password == "" and btn_next:
                    st.warning('Please enter your email address and password.')
                    
                elif password == "" and student_id != "" and email != "" and btn_next:
                    st.warning('Please enter your password.')
                  
                elif password == "" and student_id == "" and email == "" and btn_next:
                    st.warning("Please enter your student id, email address and password.")
                    
                elif password != "" and student_id != "" and email != "" and btn_next and valid == True and checkbox_next:
                    st.success('This email address is available for sign up!')
                    st.info('Continuing to face recognition process...')
                    
                elif password != "" and student_id != "" and email != "" and btn_next and valid == True and not checkbox_next:
                    st.info('Please agree and continue to your password.')

    
        #Button for re-direct to the login page
        if st.button('Login'):
            self.set_access(0, None)  
            self.do_redirect()
    
                
        with col2:
            
            #Face recognition part
           
            if 'frame' not in st.session_state:
                st.session_state.frame = None
                
            if 'img_name' not in st.session_state:
                st.session_state.img_name = None
                 
            if student_id != "" and email != "" and password != "" and checkbox_next: 
                
                st.header('Face Recognition')
                #Display for ensuring the correct account to sign up
                st.markdown("Student ID: {}".format(st.session_state.student_id))
                st.markdown("Email Address: {}".format(st.session_state.email))
                    
                st.info('Please agree and continue to face recognition')
                
                run = st.checkbox('Agreed to open your camera?', key = 'run')
                
                FRAME_WINDOW = st.image([])
                
                #Initialize the camera (webcam) using the VideoCapture() method
                camera = cv2.VideoCapture(0)
                 
                #if run:
                st.warning("Please face the camera before submit... ")
                # btn_capture = st.button('Capture Now' , on_click=self.reset_checkbox)
                
                btn_sign_up = st.button('Submit and Sign Up', on_click=self.reset_checkbox)
                
                while run:
                    #Read input using the camera using the camera.read() method.
                    _, st.session_state.frame = camera.read()
                    #When code is cv2.COLOR_BGR2RGB, BGR (Blue, green, red) is converted to RGB.
                    #when converted to RGB, it will be saved as a correct image to display on the window frame.
                    st.session_state.face = cv2.cvtColor(st.session_state.frame, cv2.COLOR_BGR2RGB)
                    FRAME_WINDOW.image(st.session_state.face)
                    
                    #Click 'submit and sign up' to capture your face
                    if btn_sign_up:
                        break
 
                if btn_sign_up:
                    #set the image file format to save into
                    st.session_state.img_name = "user_{}.png".format(st.session_state.email)
                    #Display the converted captured image into the window frame
                    st.image(st.session_state.face, caption=st.session_state.img_name)
                    
                    #save the captured image with image file format
                    cv2.imwrite(st.session_state.img_name, st.session_state.frame)
                    #save the captured image file into firebase storage with the path: faces/user_{}.png
                    st.session_state.storage.child('faces').child(st.session_state.email).child(st.session_state.img_name).put(st.session_state.img_name)
                    print('\nCreated Face Recognition: ' + st.session_state.img_name +'\n')
                    st.success('Sign up successfully!')
                    print("\nSigned up as " + st.session_state.email + " successfully. \n")
                    # After the account is registered, it will re-direct to the login page
                    self.set_access(0, None)  
                    self.do_redirect()
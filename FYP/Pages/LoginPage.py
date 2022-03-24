# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 20:53:17 2022

@author: Loo Jia Wen 0129868
"""

#Import modules
import streamlit as st
from hydralit import HydraHeadApp
import cv2
import smtplib  # sending emails using the Simple Mail Transfer Protocol
from datetime import datetime
from deepface import DeepFace


class LoginPage(HydraHeadApp): 
    
    def reset_checkbox(self):
        st.session_state.run = False            
    
    
    def run(self):
        
        st.title('Student Information System')
        col1, col2 = st.columns(2)
        
        with col1:
            # Password login form
            # Prevent page refresh after one input
            with st.form(key='login_form'):
                st.header('Login')
                email = st.text_input("Email Address: ", "eg: 01XXXXX@kdu-online.com", key='email') 
                password = st.text_input("Password: ", type="password", key='password')
                checkbox_next = st.checkbox('Confirm your password?', key='checkbox_next')
                btn_next = st.form_submit_button(label='Next')
                
            index = None
            
            if btn_next:
                exists = (st.session_state.users['email'] == email).any()
                #st.write(st.session_state.users)
                if exists:
                    valid_credentials = st.session_state.auth.sign_in_with_email_and_password(email, password)
                    
                    if valid_credentials:
                        
                        index = st.session_state.users.index
                        user_indices = index[(st.session_state.users['email'] == email) & (st.session_state.users['password'] == password)]
                        index = user_indices.tolist()
                        index = index[0]
                        st.info('Proceeding to face recognition')
                        print('\nEntered email and password are valid.\n')
                        print('Proceeding to face recognition...\n')
                        
                    else:
                        st.warning('Entered wrong email or password.')
                        self.session_state.allow_access = 0
                        self.session_state.current_user = None
                        
                else:
                    st.error('This Account is not registered yet.')
                                        
    
            if st.button('Sign Up'):
                self.set_access(-1, 'guest')
                self.do_redirect()
                
        with col2:
            
            if 'frame' not in st.session_state:
                st.session_state.frame = None
                
            if 'img_name' not in st.session_state:
                st.session_state.img_name = None
                 
            if email != "" and password != "" and checkbox_next: 

                st.header('Face Recognition')
                st.markdown("Email Address: {}".format(st.session_state.email))
                
                st.info('Please agree and continue to face recognition')
                
                run = st.checkbox('Agreed to open your camera?', key = 'run')
        
                FRAME_WINDOW = st.image([])
                
                #Initialize the camera (webcam) using the VideoCapture() method
                camera = cv2.VideoCapture(0)

                st.warning("Please face the camera while capturing... ")
                btn_login = st.button('Login', on_click=self.reset_checkbox)
                
                verify_face = False
                
                while(run):
                    #Read input using the camera using the camera.read() method.
                    ret, st.session_state.frame = camera.read()
                    
                    #When code is cv2.COLOR_BGR2RGB, BGR (Blue, green, red) is converted to RGB.
                    #when converted to RGB, it will be saved as a correct image to display on the window frame.
                    st.session_state.face = cv2.cvtColor(st.session_state.frame, cv2.COLOR_BGR2RGB)
                    FRAME_WINDOW.image(st.session_state.face)
                    
                    # Click 'login' to capture, recognize and verify your login face
                    if btn_login:
                        break
                
                if btn_login:
                    #set and save the captured image with a image file format
                    st.session_state.img_name = "login_{}.png".format(st.session_state.email)
                    current_face = cv2.imwrite(st.session_state.img_name, st.session_state.frame)
                    #save the image file into firebase storage with the path: faces/user_{}.png
                    st.session_state.storage.child('faces').child(st.session_state.email).child(st.session_state.img_name).put(st.session_state.img_name)
                    st.info('Recognizing your face...')
                    #st.image(st.session_state.img_name)
                    
                    #Retrieve the image (login face) from a file
                    current_face = "login_{}.png".format(st.session_state.email)
                    #The path of the image (login face)
                    login_image_url_path = st.session_state.storage.child('faces').child(st.session_state.email).child(current_face).get_url(current_face)
                    
                    #Retrieve the image (signup face) from a file
                    user_face = "user_{}.png".format(st.session_state.email)
                    #The path of the image (signup face)
                    signup_image_url_path = st.session_state.storage.child('faces').child(st.session_state.email).child(user_face).get_url(user_face)
                    
                    
                    #**********The step of verifying the login user face (using ArcFace model)*********
                    #ArcFace is an open source state-of-the-art model for facial recognition.
                    #ArcFace is a machine learning model that takes two face images 
                    #as input and outputs the distance between them to see how likely they are to be the same person.
                    #The distance between faces is calculated using cosine distance, which is a method used by search engines
                    #and can be calculated by the inner product of two normalized vectors. 
                    #If the two vectors are the same, θ will be 0 and cosθ=1. If they are orthogonal, θ will be π/2 and cosθ=0. 
                    #Therefore, it can be used as a similarity measure.
                    model_name = 'ArcFace'
                    verify_face = DeepFace.verify(img1_path = signup_image_url_path, img2_path = login_image_url_path, model_name = model_name)
                    run = False
                
                    #Correct email, password and login face
                    if verify_face['verified'] == True:
                        
                        st.success('Logged in as {} successfully.'.format(st.session_state.email))
                        print("\nLogged in as " + st.session_state.email + " successfully.")
                        print("\nLogin User face: ")
                        print(verify_face)
                        
                        #Send email login notification if successful login
                        #The mail address and password
                        gmail_user = 'sisteam149@gmail.com' # SIS email 
                        gmail_password = 'sis12345678'
                        
                        user_email = st.session_state.email  #login user email
                        email_title = '**ALERT: SIS Login Notification**'
                              
                        #setup the mail
                        sent_from = gmail_user
                        to = user_email
                        subject = email_title
                        body = '\n\nHi there,\n\nThis is '+ email_title + '. Someone just used your SIS account to login. \n\nIf this person was logged in without your permission, please take action immediately, then change your password and face recognition to protect your account. \n\nIf this was an authorized login, please ignore this email. \n\n\nThanks, \nThe SIS Team'
                        message = 'Subject: {}\n\n{}'.format(subject, body)
           
                        try:
                            #Create SMTP session for sending email
                            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465) #use gmail with port
                            smtp_server.ehlo() #enable security
                            smtp_server.login(gmail_user, gmail_password) # login with gmail id and password
                            smtp_server.sendmail(sent_from, to, message) #mail content
                            smtp_server.close()
                            print ("\nEmail login notification sent successfully to the user!")
                        except Exception as ex:
                            print ("\nFailed to send the email, something went wrong…",ex)
                       
                        self.set_access(1, email)
                        st.session_state.current_user = st.session_state.users[st.session_state.users['email'] == email].to_dict('records')[0]
                        #Record login time 
                        now = datetime.now()
                        login_time = now.strftime("%d/%m/%Y %H:%M:%S")
                        st.session_state.db.child('users').child(st.session_state.current_user['user_id']).update({"login_time": login_time})
                        print ("\nUser login successfully.\n")
                        self.do_redirect()
                         
                    else:
                        self.session_state.allow_access = 0
                        self.session_state.current_user = None
                        st.warning('Unable to recognize your face. Try Again.')
                        print("\nLogin User face: ")
                        print(verify_face)
                        print("\nUser login failed.")
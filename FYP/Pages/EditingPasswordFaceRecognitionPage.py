# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 21:28:16 2022

@author: Loo Jia Wen 0129868
"""

#Import modules
import streamlit as st
from hydralit import HydraHeadApp
import cv2

class EditingPasswordFaceRecognitionPage(HydraHeadApp): 
    
    def reset_checkbox(self):
        st.session_state.run = False  
    
    def run(self):
        
        print('\nRunning "Change Password & Facial Recognition" page...\n')
        st.title('Change Password & Facial Recognition')
        
        #Display user information
        student_info = st.session_state.db.child("users").order_by_child("user_id").equal_to(st.session_state.current_user['user_id']).get()     
        for s in student_info.each():
            # Display user last login history
            st.subheader("Last login: " + s.val()["login_time"])
            
            choice_block = st.empty()
            choice = choice_block.radio('Change Password / FaceRecognition', ['Password', 'Face Recognition'])
            
            if choice == 'Password':
                print('\nSelecting change password...\n')
                old_password_block = st.empty()
                old_password = old_password_block.text_input("Current password: ", type="password")
                    
                new_password_block = st.empty()
                new_password = new_password_block.text_input("New password: ", type="password")
                
                enter_new_password_block = st.empty()
                enter_new_password = enter_new_password_block.text_input("Re-enter new password: ", type="password")
                    
                btn_update_password = st.button("Update Password")
                if old_password == s.val()["password"] and new_password == enter_new_password and btn_update_password:
                    st.session_state.db.child('users').child(st.session_state.current_user['user_id']).update({"password": enter_new_password})
                    st.success("New password updated successfully.")
                    print("\nNew password updated successfully.")
                    print("\nNew password: " + enter_new_password)
                    
                    # #Delete all placeholder
                    # old_password_block.empty()
                    # new_password_block.empty()
                    # enter_new_password_block.empty()
                    
                elif old_password != s.val()["password"]:
                    st.warning("Incorrect password.")

                    
                elif new_password != enter_new_password:
                    st.warning("Incorrect re-enter new password.")

                
                
            elif choice == 'Face Recognition':
                
                print('\nSelecting change face recognition...\n')
                
                if 'frame' not in st.session_state:
                    st.session_state.frame = None
                    
                if 'img_name' not in st.session_state:
                    st.session_state.img_name = None
                    
                email_face = st.text_input("Confirm your email:")
                
                if email_face == st.session_state.current_user['email']:
                    
                    st.info('Please agree and update your face recognition')
                       
                    run = st.checkbox('Agreed to open your camera?')
                    FRAME_WINDOW = st.image([])
                    
                    #Initialize the camera (webcam) using the VideoCapture() method
                    camera = cv2.VideoCapture(0)
        
                    st.warning("Please face the camera while capturing... ")
                    btn_update_face = st.button('Update Face', on_click=self.reset_checkbox)
                    
                    while(run):
                        #Read input using the camera using the camera.read() method.
                        _, st.session_state.frame = camera.read()
                        
                        #When code is cv2.COLOR_BGR2RGB, BGR (Blue, green, red) is converted to RGB.
                        #when converted to RGB, it will be saved as a correct image to display on the window frame.
                        st.session_state.face = cv2.cvtColor(st.session_state.frame, cv2.COLOR_BGR2RGB)
                        FRAME_WINDOW.image(st.session_state.face)
                        
                        # Click 'login' to capture, recognize and verify your login face
                        if btn_update_face:
                            break
                    
                    if btn_update_face:
                        #set the image file format to save into
                        st.session_state.img_name = "user_{}.png".format(email_face)
                        #Display the converted captured image into the window frame
                        st.image(st.session_state.face, caption=st.session_state.img_name)
                        
                        #save the captured image with image file format
                        cv2.imwrite(st.session_state.img_name, st.session_state.frame)
                        #save the captured image file into firebase storage with the path: faces/user_{}.png
                        st.session_state.storage.child('faces').child(st.session_state.current_user['email']).child(st.session_state.img_name).put(st.session_state.img_name)
                        run = False
                        st.success('Updated New Face Recognition.')
                        print('\nUpdated New Face Recognition: ' + st.session_state.img_name +'\n')
                        
                    
                else:
                    st.info("Please enter your email for updating face.")
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 20:50:04 2022

@author: Loo Jia Wen 0129868
"""

class CurrentUser:
    
    def _init_(self):
        self.user_id = None
        self.student_id = None
        self.email = None
        self.password = None
        self.login_time = None
        self.student_name = None
        self.ic_passport = None
        self.country = None
        self.marital_status = None
        self.contact_number = None
        self.home_address = None
        self.update_date = None
        
    def set_user(self, u):
        self.user_id = u['user_id']
        self.student_id = u['student_id']
        self.email = u['email']
        self.password = u['password']
        self.login_time = u['login_time']
        self.student_name = u['student_name']
        self.ic_passport = u['ic_passport']
        self.country = u['country']
        self.marital_status = u['marital_status']
        self.contact_number = u['contact_number']
        self.home_address = u['home_address']
        self.update_date = u['update_date']
        
    def get_user_id(self):
        return self.user_id
    
    def get_student_id(self):
        return self.student_id
    
    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password
    
    def get_login_time(self):
        return self.login_time
    
    def get_student_name(self):
        return self.student_name
    
    def get_ic_passport(self):
        return self.ic_passport
    
    def get_country(self):
        return self.country
    
    def get_marital_status(self):
        return self.marital_status
    
    def get_contact_number(self):
        return self.contact_number
    
    def get_home_address(self):
        return self.home_address
    
    def get_update_date(self):
        return self.update_date
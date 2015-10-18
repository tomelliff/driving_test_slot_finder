#!/usr/bin/python

# Looks for driving test slots for a given time period

import requests

a='TEST'
b='123456'

def create_session():
  
  # Creates a session to be used throughout

  login_url = 'https://driverpracticaltest.direct.gov.uk/login'
  
  s = requests.Session()

  s.get(login_url)

  return s 

def login(session, driving_licence_num, application_ref_num):

  # Logs in to the driving test management portal
  # with provided credentials

  s = session

  login_url = 'https://driverpracticaltest.direct.gov.uk/login'
  login_details = {
    'username': driving_licence_num,
    'password': application_ref_num
  }
  other_form_data = {
    'javascriptEnabled': 'true',
    'passwordType': 'NORMAL',
    'alternativePassword': '',
    'booking-login': 'Continue'
  }

  form_data = login_details.copy()
  form_data.update(other_form_data)

  r = s.post(login_url, data=form_data)

  return r

#cookies = create_session().cookies

session = create_session()
login = login(session,a,b)

print(login.text)
print('')
print(session.cookies)

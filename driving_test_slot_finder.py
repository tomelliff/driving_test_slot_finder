#!/usr/bin/python

# Looks for driving test slots for a given time period

import requests

a='TEST'
b='123456'

def login(driving_licence_num, application_ref_num):

  # Logs in to the driving test management portal
  # with provided credentials

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

  r = requests.post(login_url, data=form_data)

  return r

login = login(a,b)

print(login.text)

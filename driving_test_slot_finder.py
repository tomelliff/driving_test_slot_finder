#!/usr/bin/python

# Looks for driving test slots for a given time period

import ConfigParser
import re
import sys

from bs4 import BeautifulSoup
import requests

config = ConfigParser.RawConfigParser()
config.read('properties.cfg')

driving_licence_num = config.get('credentials', 'driving_licence_number')
application_ref_num = config.get('credentials', 'application_reference_number')

def create_session():
  
  # Creates a session to be used throughout
  # Returns session object and boolean capctcha_present

  login_url = 'https://driverpracticaltest.direct.gov.uk/login'
  
  s = requests.Session()

  r = s.get(login_url)

  captcha_present = check_for_captcha(r.text)
  
  return s, captcha_present

def login(session, driving_licence_num, application_ref_num):

  # Logs in to the driving test management portal with provided credentials
  # Returns request object

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

def check_for_captcha(html):

  # Checks for captcha element
  # Returns boolean - True if recaptcha-check element is present

  html_soup = BeautifulSoup(html, 'html.parser')
  captcha_challenge = html_soup.find(id='recaptcha-check')

  if captcha_challenge is None:
    captcha = False
  else:
    captcha = True

  return captcha


### Use functions

session, captcha_present = create_session()

# Only login if captcha not present on login page
if not captcha_present:
  login = login(session, driving_licence_num, application_ref_num)
  print(login.text)
  csrf_search = re.search('csrftoken=(.*)&amp', login.text)
  if csrf_search is not None:
    csrf = csrf_search.group(1)
    print(csrf)
  else:
    print('CSRF token not found')
else:
  print('Captcha challenge detected, exiting')
  sys.exit(1)

####################################################################
# Skeleton for Selenium tests on Sauce Labs
####################################################################

###################################################################
# Imports that are good to use
###################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os
import urllib3
import json
import random
from colorama import Fore, Back, Style

###################################################################
# Selenium with Python doesn't like using HTTPS correctly
# and displays a warning that it uses Unverified HTTPS request
# The following disables that warning to clear the clutter
# But I should find a way to do the proper requests
###################################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###################################################################
# Pull a random Pokemon name to use as the test name
###################################################################
pokemon_names_url = urllib3.PoolManager().request('GET', 'https://raw.githubusercontent.com/sindresorhus/pokemon/master/data/en.json')
pokemon_names = json.loads(pokemon_names_url.data.decode('utf-8'))
random_pokemon = random.choice(pokemon_names)

###################################################################
# Select Data Center
# Set region to 'US' or 'EU'
# Test will default to 'US' if left blank or set to any other than 'US' or 'EU'
###################################################################
region = 'US'

###################################################################
# Common parameters (desired capabilities)
###################################################################
sauceParameters = {
    'platformName': 'MacOS 12',
    'browserName': 'chrome',
    'browserVersion': 'latest',

    # Sauce Specific Options
    'sauce:options':{
        'tags':['Repro Attempt'],
        'name': 'NFP Desktop Example',
        'screenResolution':'1440x900',
        'seleniumVersion': '4',
        # 'tunnelIdentifier': '',
        # 'extendedDebugging': True,
        # 'capturePerformance': 'true',
        # 'idleTimeout': 180,
        # 'commandTimeout': 600,
    },
}

# This concatenates the tags key above to add the build parameter
sauceParameters['sauce:options'].update({'build': '-'.join(sauceParameters['sauce:options'].get('tags'))})

###################################################################
# Connect to Sauce Labs
try:
    region
except NameError:
    region = 'EU'

if region == 'US':
    print(Fore.MAGENTA + 'You are using the US data center for a Desktop test, rockstar!' + Style.RESET_ALL)
    driver = webdriver.Remote(
        command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.us-west-1.saucelabs.com:443/wd/hub',
        desired_capabilities=sauceParameters)
elif region == 'EU':
    print (Fore.CYAN + 'You are using the EU data center for a Desktop test, you beautiful tropical fish!' + Style.RESET_ALL)
    driver = webdriver.Remote(
        command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.eu-central-1.saucelabs.com:443/wd/hub',
        desired_capabilities=sauceParameters)
elif region == 'APAC':
    print (Fore.BLUE + 'You are using the APAC data center for a Desktop test! Shiny and new!' + Style.RESET_ALL)
    driver = webdriver.Remote(
        command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.apac-southeast-1.saucelabs.com:443/wd/hub',
        desired_capabilities=sauceParameters)
###################################################################
# Test logic goes here
###################################################################
# Navigating to a website
driver.get('https://www.nfp.com')


#Finding the locations element
locations = driver.find_element(By.CLASS_NAME,'fa-building')
sleep(2)

# clicking on the selected element
locations.click()
sleep(4)

#Finding the search bar
search = driver.find_element(By.ID,'mobileOfficeSearchBar')
# clicking the search bar
search.click()
#searching for Austin, Texas
search.send_keys('Austin, Texas')
sleep(2)

# Finding the submit button
srchBtn = driver.find_element(By.ID,'mobileOfficeSearchBtn')

# cliking the submit button
srchBtn.click()
sleep(2)

#I found a user experience that isn't ideal, if you search Austin, Texas, it shows no results were found
noResults = driver.find_element(By. CLASS_NAME, 'alert-danger')

# Using Actions to scroll to element
ActionChains(driver).move_to_element(noResults).perform()


sleep(5)

# Setting the job status to passed
driver.execute_script('sauce:job-result=passed')

# Ending the test session
driver.quit()

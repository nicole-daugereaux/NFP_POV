####################################################################
# Skeleton for Appium tests on Sauce Labs Real Devices - Unified Platform
# This is currently in BETA and will only work for private devices
####################################################################

###################################################################
# Imports that are good to use
###################################################################
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import multiprocessing
from time import sleep
import os
import urllib3
import json
import random
import sys
from colorama import Fore, Back, Style

###################################################################
# This makes the functions below execute 'run' amount of times
###################################################################
run = 10

###################################################################
# Declare as a function in order to do multiple runs
###################################################################
def run_sauce_test():
    #Choose which platform versoin you'd like tests to use here!
    androidTest = False
    iosTest = True
    useApp = False
    # appLocation = 'storage:3d99766b-73a6-4623-9ddb-45e0454f6610'
    # appLocation = 'storage:filename=NetworkSpeed 2.zip'

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
    # pokemon_names_url = urllib3.PoolManager().request('GET', 'https://raw.githubusercontent.com/sindresorhus/pokemon/master/data/en.json')
    # pokemon_names = json.loads(pokemon_names_url.data.decode('utf-8'))
    # random_pokemon = random.choice(pokemon_names)
    
    

    ###################################################################
    # Select Data Center
    # Set region to 'US' or 'EU'
    # Test will default to 'US' if left blank or set to any other than 'US' or 'EU'
    ###################################################################
    region = 'US'

    ###################################################################
    # Common parameters (capabilities)
    ###################################################################
    projectParameters = {

        }

    androidParameters = {
    #define Android parameters here
            'browserName': 'Chrome',
            'platformName': 'Android',
            # 'appium:platformVersion': '11',
            'appium:deviceName' : 'Google.*',
            'appium:automationName': 'uiautomator2',
            'sauce:options':{
                'name': 'NFP Example Real Device Test',
                'appiumVersion': '2.0.0',
                'phoneOnly' : True,
                # ''tunnelIdentifier': 'exampletunnel'
                }
    }

    iosParameters = {
    # Define iOS Parameters here
        'appium:deviceName' : 'iPhone.*',
        'platformName' : 'iOS',
        'appium:platformVersion': '15',
        'browserName' : 'safari',
        'appium:automationName': 'XCUITest',
        'sauce:options':{
            'name': 'NFP Example Real Device Test',
            'appiumVersion': '2.0.0',
        },
    }

    ###################################################################
    # Merge parameters into a single capability dictionary

    ###################################################################
    sauceParameters = {}
    if androidTest != True and iosTest != True:
        print('You need to specify a platform to test on!')
        sys.exit()
    elif androidTest == True and iosTest == True:
        print('Don\'t be greedy! Only choose one platform!')
        sys.exit()
    elif androidTest:
        sauceParameters.update(androidParameters)
        if useApp:
            sauceParameters['app'] = appLocation # Use app if it's specified
        else:
            sauceParameters['browserName'] = 'Chrome' # Otherwise use Chrome
            #Note! Replace 'Chrome' with 'Browser' for older versions of Android to use the stock browser
    elif iosTest:
        sauceParameters.update(iosParameters)
        if useApp:
            sauceParameters['app'] = appLocation
        else:
            sauceParameters['browserName'] = 'safari'



    # This concatenates the tags key above to add the build parameter
    sauceParameters.update({'build': 'Investigation'})

    ###################################################################
    # Connect to Sauce Labs
    ###################################################################
    try:
        region
    except NameError:
        region = 'US'

    if region != 'EU':
        print(Fore.MAGENTA + 'You are using the US data center for an RDC test, so a bald eagle is obviously running your tests.' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.us-west-1.saucelabs.com:443/wd/hub',
            desired_capabilities=sauceParameters)
    elif region == 'EU':
        print (Fore.CYAN + 'You are using the EU data center for an RDC test, you beautiful tropical fish!' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.eu-central-1.saucelabs.com:443/wd/hub',
             desired_capabilities=sauceParameters)

    ###################################################################
    # Test logic goes here
    ###################################################################

    # Navigating to a website
    driver.get('https://www.nfp.com')
    # sleep(2)

    # driver.CONTEXTS()
    # driver.switch_to.context('WEBVIEW_1')
    #Click hamburger menu button
    toggler = driver.find_element(AppiumBy.CLASS_NAME, 'navbar-toggler')
    sleep(2)
    toggler.click()
    sleep(2)

    #Finding the locations element
    locations = driver.find_element(AppiumBy.CLASS_NAME,'fa-building')
    sleep(2)

    # clicking on the selected element
    locations.click()
    sleep(2)

    #Finding the search bar
    search = driver.find_element(AppiumBy.ID,'mobileOfficeSearchBar')
    search.send_keys('Austin, Texas')
    sleep(2)

    # Finding the submit button
    srchBtn = driver.find_element(AppiumBy.ID,'mobileOfficeSearchBtn')

    # cliking the submit button
    srchBtn.click()
    sleep(4)

    #move seach bar into view

    # # Setting the job status to passed
    driver.execute_script('sauce:job-result=passed')
    #
    # # Ending the test session
    driver.quit()
if __name__ == '__main__':
    jobs = [] # Array for the jobs
    for i in range(run): # Run the amount of times set above
        jobRun = multiprocessing.Process(target=run_sauce_test) # Define what function to run multiple times.
        jobs.append(jobRun) # Add to the array.
        jobRun.start() # Start the functions.
        # print('this is the run for: '+ str(i))

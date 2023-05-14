"""
Here I test scrolling in mobile devices using Appium.
"""


from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
import time


def test_open_support():
    desired_cap = {
        'deviceName': 'emulator-5554',  # Emulated Pixel 3 API 29
        'platformName': 'Android',
        'appPackage': 'com.itrustore.ratengoods',
        'appActivity': 'com.itrustore.ratengoods.main.XMainActivity'
    }
    driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub", desired_capabilities=desired_cap)
    action = TouchAction(driver)
    # Open the Menu
    try:
        driver.find_element_by_xpath("//*[@content-desc='Drawer open']").click()
    except (NoSuchElementException, TimeoutException):
        action.press(x=200, y=200).release().perform()
        time.sleep(5)
        driver.find_element_by_xpath("//*[@content-desc='Drawer open']").click()
    # Find an element to scroll from
    receipts = driver.find_element_by_xpath("//*[@text='Receipts']")
    # Give the values for x and y to move from the defined element (here - receipts)
    action.press(receipts).move_to(x=0, y=100).release().perform()
    # time just for visual check that scrolling occured
    time.sleep(5)
    driver.find_element_by_xpath("//*[@text='Ask support']").click()
    # time just for visual check that the support menu was opened
    time.sleep(5)

    driver.quit()

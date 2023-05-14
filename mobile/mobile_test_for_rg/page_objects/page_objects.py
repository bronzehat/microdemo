from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.touch_action import TouchAction
import time


class RG_Android():

    def __init__(self, driver):
        self.driver = driver

    def open_search(self):
        touch = TouchAction(self.driver)
        try:
            self.driver.find_element_by_id("com.itrustore.ratengoods:id/search").click()
        except (NoSuchElementException, TimeoutException):
            touch.press(x=200, y=200).release().perform()
            time.sleep(5)
            self.driver.find_element_by_id("com.itrustore.ratengoods:id/search").click()
        self.driver.find_element_by_id("com.itrustore.ratengoods:id/search_hint").click()

    def find_product(self, product):
        search_editor = self.driver.find_element_by_id("com.itrustore.ratengoods:id/search_editor")
        search_editor.send_keys(product)
        self.driver.find_element_by_xpath("//*[@text='{}']".format(product)).click()

    def get_product_rating(self):

        return self.driver.find_element_by_id("com.itrustore.ratengoods:id/rating").text

    def open_settings(self):
        touch = TouchAction(self.driver)
        try:
            self.driver.find_element_by_xpath("//*[@content-desc='Drawer open']").click()
        except (NoSuchElementException, TimeoutException):
            touch.press(x=200, y=200).release().perform()
            time.sleep(5)
            self.driver.find_element_by_xpath("//*[@content-desc='Drawer open']").click()
            try:
                self.driver.find_element_by_xpath("//*[@text='Settings']").click()
            except (NoSuchElementException, TimeoutException):
                actions = TouchAction(self.driver)
                actions(10, 100)
                actions.perform()
                self.driver.find_element_by_xpath("//*[@text='Settings']").click()

    def profile_id(self):
        return self.driver.find_element_by_id("com.itrustore.ratengoods:id/profile_id").text

    def build_version(self):
        return self.driver.find_element_by_id("com.itrustore.ratengoods:id/settings_version").text

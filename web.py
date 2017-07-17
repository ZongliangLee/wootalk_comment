#!/usr/bin/python
# -*- coding: utf-8 -*-  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from msg import msg



class Wootalk():
    def setUp(self,responseTime):
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "http://Wootalk.today"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.responseTime = responseTime  
    
    def launch(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("startButton").click()
        message_sent = False
        i = 0
        while 1:
            texts = len(driver.find_elements_by_xpath("//div[@class=\"system text \"]"))
            if (texts==4 or texts==6 or texts==8) and not message_sent:
                driver.find_element_by_id("messageInput").clear()
                driver.find_element_by_id("messageInput").send_keys(msg)
                driver.find_element_by_css_selector("#sendButton > input[value=\"傳送\"]").click()
                driver.find_element_by_xpath("//div[@class=\"me text\"]")
                print '留下聯絡方式完成'
                i = 0
                message_sent = True

            elif texts ==5 or texts ==7 or texts ==9:
                print '對方離開'
                driver.find_element_by_css_selector("#changeButton > input[value=\"離開\"]").click()
                time.sleep(1)
                driver.find_element_by_id("startButton").click()
                i = 0
                message_sent = False

            else:
                 print i
                 time.sleep(1)
                 i=i+1
                 if i == self.responseTime:
                    print '超過時間,換人!'
                    driver.find_element_by_css_selector("#changeButton > input[value=\"離開\"]").click()
                    driver.find_element_by_id("popup-yes").click()
                    time.sleep(1)
                    driver.find_element_by_id("startButton").click()
                    i = 0
                    message_sent = False
                    # return '超過時間,換人!'

    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def close(self):
        self.driver.quit()
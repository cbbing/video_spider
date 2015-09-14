#encoding: utf-8

import time
import requests
from pandas import Series, DataFrame

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

driver = webdriver.PhantomJS()
driver.get("http://login.weibo.cn/login/")


driver.find_element_by_xpath('//input[@name="mobile"]').send_keys('cbb6150')
driver.find_element_by_xpath('//input[@type="password"]').send_keys('xx.785906')
time.sleep(2)
driver.get_screenshot_as_file('show.png')
driver.find_element_by_xpath('//input[@name="submit"]').click()

try:
    dr = WebDriverWait(driver, 5)
    dr.until(lambda the_driver:the_driver.find_element_by_xpath('//span[@class="tc"]').is_displayed())
except Exception,e:
    print str(e)
    print 'fail login in'
    sys.exit(0)

driver.get_screenshot_as_file('show2.png')

driver.find_element_by_link_text("下页").click();#点击链接
time.sleep(2)
driver.get_screenshot_as_file('show3.png')
f = open('data.html','w')
f.write(driver.page_source)
f.close()
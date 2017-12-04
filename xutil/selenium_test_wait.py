# -*- coding: utf-8 -*-
__author__ = 'Vit'
from time import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start=time()


driver = webdriver.Chrome()
# driver.get("https://www.porntube.com/videos/via-lasciva-dp-trio-painters_7282989")
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "video"))
#     )
#     print(element.get_attribute('src'))
# finally:
#     driver.quit()


driver.implicitly_wait(10) # seconds
driver.get("https://www.porntube.com/videos/via-lasciva-dp-trio-painters_7282989")
element = driver.find_element_by_tag_name("video")
print(element.get_attribute('src'))

print('Parsing time {0:.2f} s'.format(time() - start))
driver.quit()
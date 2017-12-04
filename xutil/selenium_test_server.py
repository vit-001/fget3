# -*- coding: utf-8 -*-
__author__ = 'Vit'

from selenium import webdriver
from time import time


if __name__ == "__main__":
    from selenium.webdriver.common.keys import Keys

    start = time()

    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)




    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')

    # driver=webdriver.Chrome()
    # driver2=webdriver.Chrome()
    # driver=webdriver.PhantomJS()
    driver.minimize_window()
    driver.get("https://www.porntube.com/videos/blonde-teenie-playing-banana-webcam_7263947")

    # assert "Python" in driver.title

    # elem=driver.fi
    elem = driver.find_element_by_tag_name("video")
    print(elem.get_attribute('src'))


    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source

    print('Parsing time {0:.2f} s'.format(time() - start))

    driver.close()


    pass
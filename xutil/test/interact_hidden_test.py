# -*- coding: utf-8 -*-
__author__ = 'Vit'

import os
import sys


from time import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup


if __name__ == "__main__":
    start = time()
    from selenium.webdriver.common.keys import Keys



    # options = webdriver.ChromeOptions()
    #  options.add_argument('--headless')

    # options=webdriver.FirefoxOptions()
    # options.set_headless(True)

    os.environ['MOZ_HEADLESS'] = '1'

    # Select your Firefox binary.
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)

    # Start selenium with the configured binary.
    driver = webdriver.Firefox(firefox_binary=binary)
    # driver2=webdriver.Chrome()
    # driver=webdriver.PhantomJS()
    # driver.minimize_window()
    driver.get("http://www.drtuber.com/video/4082638/teen-tied-and-made-to-cum-big-booty-amateur-fuck")

    # assert "Python" in driver.title

    # elem=driver.fi
    # elem = driver.find_element_by_tag_name("video")
    # print(elem.get_attribute('src'))

    soup=BeautifulSoup(driver.page_source, 'lxml')

    player=soup.find('div',{'class':'player'})

    print(player.prettify())

    fullscreen_bn=driver.find_element_by_class_name('drt-button-fullscreen')
    play_bn=driver.find_element_by_class_name('drt-button-play')
    enter_bn=driver.find_element_by_class_name('modal_btn')
    quality_bn=driver.find_element_by_class_name('drt-button-quality')

    print(play_bn.text)

    actions = ActionChains(driver)
    # actions.move_to_element(enter_bn)
    actions.click(enter_bn)
    actions.click(play_bn)
    actions.click(quality_bn)
    actions.perform()


    print('================================================================================================')
    print('================================================================================================')
    print('================================================================================================')

    soup=BeautifulSoup(driver.page_source, 'lxml')

    player=soup.find('div',{'class':'player'})

    print(player.prettify())


    # hq_button=driver.fi


    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source

    print('Parsing time {0:.2f} s'.format(time() - start))

    driver.quit()

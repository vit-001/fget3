# -*- coding: utf-8 -*-
__author__ = 'Vit'
from time import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

from common.util import _iter

def parce(soup):
    container = soup.find('div', {'id': 'player'})
    if container:
        for source in _iter(container.find_all('source')):
            print(source.attrs['data-quality'], source.attrs['src'])
            # self.set_default_video(-1)

def click(driver, bn_class):
    element=driver.find_element_by_class_name(bn_class)
    actions = ActionChains(driver)
    actions.click(element)
    actions.perform()



if __name__ == "__main__":
    start = time()
    from selenium.webdriver.common.keys import Keys



    # options = webdriver.ChromeOptions()
    #  options.add_argument('--headless')

    # options=webdriver.FirefoxOptions()
    # options.set_headless(True)

    driver=webdriver.Chrome()
    # driver2=webdriver.Chrome()
    # driver=webdriver.PhantomJS()
    # driver.minimize_window()
    driver.get("http://www.drtuber.com/video/4082638/teen-tied-and-made-to-cum-big-booty-amateur-fuck")

    # assert "Python" in driver.title

    # elem=driver.fi
    # elem = driver.find_element_by_tag_name("video")
    # print(elem.get_attribute('src'))

    soup=BeautifulSoup(driver.page_source, 'lxml')
    parce(soup)

    # player=soup.find('div',{'class':'player'})
    #
    # print(player.prettify())

    # fullscreen_bn=driver.find_element_by_class_name('drt-button-fullscreen')
    # play_bn=driver.find_element_by_class_name('drt-button-play')
    # enter_bn=driver.find_element_by_class_name('modal_btn')
    # quality_bn=driver.find_element_by_class_name('drt-button-quality')
    #
    # print(play_bn.text)
    #
    # actions = ActionChains(driver)
    # # actions.move_to_element(enter_bn)
    # actions.click(enter_bn)
    # actions.click(play_bn)
    # actions.click(quality_bn)
    # actions.perform()

    player=driver.find_element_by_class_name('player')

    click(driver, 'modal_btn')
    click(driver, 'drt-button-play')
    click(driver, 'drt-button-quality')


    # print('================================================================================================')
    # print('================================================================================================')
    # print('================================================================================================')

    soup=BeautifulSoup(driver.page_source, 'lxml')

    parce(soup)

    # player=soup.find('div',{'class':'player'})
    #
    # print(player.prettify())


    # hq_button=driver.fi


    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source

    print('Parsing time {0:.2f} s'.format(time() - start))

    print('current', driver.current_window_handle)

    current=driver.current_window_handle

    for handle in driver.window_handles:
        print(handle)
        if handle != current:
            driver.switch_to.window(handle)
            driver.close()

        driver.switch_to.window(current)

        print('current', driver.current_window_handle)


    # driver.quit()

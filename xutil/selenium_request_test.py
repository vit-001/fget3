# -*- coding: utf-8 -*-
__author__ = 'Vit'
from time import time
from selenium import webdriver
from seleniumrequests import Ie


if __name__ == "__main__":
    start = time()
    from selenium.webdriver.common.keys import Keys



    # options = webdriver.ChromeOptions()
    #  options.add_argument('--headless')

    # options=webdriver.FirefoxOptions()
    # options.set_headless(True)

    driver=Ie()
    driver.minimize_window()
    # driver2=webdriver.Chrome()
    # driver=webdriver.PhantomJS()
    # driver.minimize_window()
    # driver.get("https://www.porntube.com/videos/via-lasciva-dp-trio-painters_7282989")

    #
    #
    # # assert "Python" in driver.title
    #
    # # elem=driver.fi
    # elem = driver.find_element_by_tag_name("video")
    # print(elem.get_attribute('src'))
    # print(driver.page_source)
    #
    #
    # # elem.send_keys("pycon")
    # # elem.send_keys(Keys.RETURN)
    # # assert "No results found." not in driver.page_source
    #
    # print('Parsing time {0:.2f} s'.format(time() - start))
    #
    # start = time()
    #
    # driver.get("http://www.pornfapr.com/videos/15243/hot-single-mom-with-big-boobs-reagan-foxx-had-a-wild-sex-action-with-two-young-guys/")
    #
    # # assert "Python" in driver.title
    #
    # # elem=driver.fi
    # elem = driver.find_element_by_tag_name("video")
    # print(elem.get_attribute('src'))

    response=driver.request('GET',"http://www.pornfapr.com/videos/15243/hot-single-mom-with-big-boobs-reagan-foxx-had-a-wild-sex-action-with-two-young-guys/")

    print(response)


    print('Parsing time {0:.2f} s'.format(time() - start))

    driver.close()











    driver.close()


    pass
# -*- coding: utf-8 -*-
__author__ = 'Vit'

import os
import sys
import io

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

def load(url, fname, cookies=None, headers=None, proxies=None):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"

    print('Loading', url, 'to', fname)

    # Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.
    os.environ['MOZ_HEADLESS'] = '1'

    # Select your Firefox binary.
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)

    # Start selenium with the configured binary.
    driver = webdriver.Firefox(firefox_binary=binary)

    # Visit this webpage.
    driver.get(url)

    # print(driver.page_source)

    # buf = io.StringIO(driver.page_source)
    try:
        with open(fname, 'w', errors='ignore') as fd:
            # chunk = buf.read(256)
            # while len(chunk) > 0:
                fd.write(driver.page_source)
                # chunk = buf.read(256)
    except FileNotFoundError as err:
        print(err)


    #
    # elem = driver.find_element_by_tag_name("source")
    # print(elem.get_attribute('src'))

    # print(driver.page_source)

    driver.quit()


    print('loaded ok!')


if __name__ == "__main__":
    url1 = 'https://yourporn.sexy/'
    url1a = 'http://pornhd8k.me/movies/big-butts-like-it-big-brazzers-whitney-wright-jake-adams-does-this-make-my-booty-look-big-31-1-2018'
    url2 = 'https://www230.playercdn.net/186/3/53wIXy8vcsQLFP-l9bGoag/1513359647/171211/355FMCV4PK0ZWON0FXZFS.mp4'
    url3 = 'http://www4.pornfun.com/remote_control.php?time=1490688627&cv=cb90ade678228733e045b68465b6f1a6&lr=0&cv2=c1451132bb5e338af902bc1c75302b82&file=%2Fcontents%2Fvideos%2F27000%2F27100%2F27100.mp4&cv3=becb9c8a2b412ea8f3fe2e3541341d4b'

    fname1 = 'out/1.html'
    fname1a = 'out/1a.html'
    fname1b = 'out/1b.html'
    fname1c = 'out/1.html'
    fname2 = 'out/1.mp4'
    fname2a = 'out/2.html'
    fname3 = 'out/3.json'
    fname4 = 'out/1.js'


    # coockies={'_gat':'1', 'protect':'BPJvGkuwOdy0D4amF44YTA', '_ga':'GA1.2.638382635.1487974825'}

    # headers = {'Referer': 'https://www.strdef.world/1cvJt-y'}

    # r=load(url1,fname1)#, proxies=proxies)
    # r = load(url2, fname2a)
    # r = load(url1a, fname1a, proxies=proxies)
    r = load(url1a, fname1a)
    # r = load(url2, fname2)#, proxies=proxies)

    # r=get_response(url3, fname2)

    # r=load('https://assets.porndig.com/assets/porndig/js/bundle.js?ver=1481122807','e:/out/bundle.js')

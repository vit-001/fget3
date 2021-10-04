# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PetardashdSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('petardashd.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/petardashd.png',
                              # menu_items=menu_items,
                              url=URL("http://petardashd.com/", test_string='porno'))

    def get_shrink_name(self):
        return 'P'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'id':'vertags'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'elementovideo'})):

                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-src',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                label = thumbnail.img.attrs.get('alt')

                duration = thumbnail.find('span', {'class': 'time'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('svg', {'class': 'hd-icon'})
                hd = '' if hd_tag is None else "HD"

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('nav',{'class':'menu-inner2'})
        if container:
            # psp(container.prettify())
            for item in _iter(container.find_all('li',{'class':'cat-item'})):
                # psp(item)
                tag=item.find('a')
                if tag:
                    # psp(tag)

                    self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'id':'vertags'})
        if container:
            for page in _iter(container.find_all('a', href= lambda x: '/tag/'in str(x))):
                self.add_page(collect_string(page), URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        # video = soup.find('div', {'id': 'mediaspace'})
        # if video:
        #     pretty(video)
            script=soup.find('script',text=lambda x: 'jwplayer' in str(x))
            # psp(script)
            if script:
                # psp(video)
                # psp(str(video))
                file=quotes(str(script).replace(' ',''), "file':'", "'")
                # psp(file)
                self.add_video('default', URL(file,base_url=url))


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # container = soup.find('div', {'class': 'video'})
        # if container:
        #     for block in _iter(container.find_all('ul',{'class':'keywords'})):
        #         # pretty(block)
                for item in _iter(soup.find_all('a', href=lambda x: '/tag/' in str(x))):
                    # pretty(item)
                    href=item.attrs.get('href','')
                    # name = item.find('span', {'itemprop': 'name'})
                    # psp(name)
                    self.add_tag(collect_string(item), URL(href, base_url=url))

        #
        # models=soup.find('div',{'class':'meta-item'})
        # if models:
        #     # pretty(models)
        #     for xref in _iter(models.find_all('a',href=lambda x: not 'javascript' in str(x))):
        #         # psp(xref)
        #         href=xref.attrs.get('href','')
        #         self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='blue'))
        #
        # categories=soup.find('div',{'class':'full-category'})
        # if categories:
        #     # pretty(categories)
        #     for xref in _iter(categories.find_all('a',href=lambda x: not 'javascript' in str(x))):
        #         # psp(xref)
        #         href=xref.attrs.get('href','')
        #         self.add_tag(collect_string(xref), URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass

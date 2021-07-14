# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class SickjunkSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('sickjunk.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/sickjunk.png',
                              # menu_items=menu_items,
                              url=URL("https://sickjunk.com/", test_string='adult'))

    def get_shrink_name(self):
        return 'SJ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # contents=soup.find('div', {'class':'content-area'})
        # # pretty(contents)
        # if contents:
            # pretty(contents)
            for thumbnail in _iter(soup.find_all('article', {'class': 'post'})):
                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True,title=True)
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    label = xref.attrs.get('title')

                    img=thumbnail.find('img', {'data-lazy-src':True})
                    # pretty(img)
                    thumb_url = URL(img.attrs.get('data-lazy-src'), base_url=url)
                #
                    duration = thumbnail.find('span', {'class': 'time'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('div', {'class': 'quality'})
                    hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text':label, 'align':'bottom center'},
                                           {'text': hd, 'align': 'top left'}])

    # def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
    #     container=soup.find('nav',{'class':'menu-inner2'})
    #     if container:
    #         # psp(container.prettify())
    #         for item in _iter(container.find_all('li',{'class':'cat-item'})):
    #             # psp(item)
    #             tag=item.find('a')
    #             if tag:
    #                 # psp(tag)
    #                 self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'page-numbers'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', src=True)
        if video:
            # pretty(video)
            self.add_video('default', URL(video.attrs['src']))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        container = soup.find('footer', {'class':'single-entry-footer'})
        if container:
            # pretty(container)
            for tag in _iter(container.find_all('a', href=True)):
                # pretty(tag)
                href = tag.attrs.get('href')
                self.add_tag(collect_string(tag), URL(href, base_url=url))
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

# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class ItsSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('its.porn/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/its.png',
                              # menu_items=menu_items,
                              url=URL("https://www.its.porn/new/", test_string='Porn'))

    def get_shrink_name(self):
        return 'I'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'thumbs'})
        # # pretty(contents)
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'thumb'})):
                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True,title=True)
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    label = xref.attrs.get('title')

                    img=thumbnail.find('img', {'data-original':True})
                    # pretty(img)
                    thumb_url = URL(img.attrs.get('data-original'), base_url=url)
                #
                    duration = thumbnail.find('span', {'class': 'time'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_tag = thumbnail.find('span', {'class': 'quality'})
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
        return soup.find('div',{'class':'pagination'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            # pretty(container)
            for page in _iter(container.find_all('a', {'href': True})):
                # pretty(page)
                if page.string:
                    # pretty(page)
                    href=page.attrs.get('href')
                    # psp(href)
                    if '#videos' in href:
                        href=quotes(str(page),'from:','"')+'/'

                    self.add_page(page.string, URL(href, base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'data-src-mp4':True})
        if video:
            # pretty(video)
            self.add_video('default', URL(video.attrs['data-src-mp4']))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        container = soup.find('div', {'class':'section_information'})
        if container:
            # pretty(container)

            for tag in _iter(container.find_all('a', href=lambda x: '/channel/' in str(x))):
                # pretty(tag)
                href = tag.attrs.get('href')
                self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='blue'))

            for tag in _iter(container.find_all('a', href=lambda x: '/model/' in str(x))):
                # pretty(tag)
                href = tag.attrs.get('href')
                self.add_tag(collect_string(tag), URL(href, base_url=url), style=dict(color='red'))

            for tag in _iter(container.find_all('a', href=lambda x: '/category/' in str(x))):
                # pretty(tag)
                href = tag.attrs.get('href')
                self.add_tag(collect_string(tag), URL(href, base_url=url))

            for tag in _iter(container.find_all('a', href=lambda x: '/tag/' in str(x))):
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

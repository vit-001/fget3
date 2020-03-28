# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class YoungPornVideosSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('youngpornvideos.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Popular=URL('https://www.youngpornvideos.com/videos/straight/all-popular.html*'),
                        Latest=URL('https://www.youngpornvideos.com/videos/straight/all-recent.html*'),
                        TopRated=URL('https://www.youngpornvideos.com/videos/straight/all-rate.html*'),
                        MostViewed=URL('https://www.youngpornvideos.com/videos/straight/all-view.html*'),
                        Longest=URL('https://www.youngpornvideos.com/videos/straight/all-length.html*'))

        view.add_start_button(picture_filename='model/site/resource/YoungPornVideos.png',
                              menu_items=menu_items,
                              url=URL("https://www.youngpornvideos.com/videos/straight/all-recent.html*", test_string='Porn'))

    def get_shrink_name(self):
        return 'YPV'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for container in soup.find_all('div',{'class':'thumb-list ac'}):
            for thumbnail in _iter(container.find_all('div',{'class':'item'})):
                xref=thumbnail.find('a')
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    img=xref.find('img')
                    description = img.attrs['alt']
                    thumb_url = URL(img.attrs.get('data-src',thumbnail.img.attrs.get('src')), base_url=url)

                    duration = thumbnail.find('span', {'class': "duration"})
                    dur_time = '' if duration is None else collect_string(duration)

                    quality = thumbnail.find('span', {'class': "flag-hd"})
                    qual = '' if quality is None else "HD"

                    for s in thumbnail.stripped_strings:
                        dur_time = s


                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'},
                                           {'text': qual, 'align': 'top left', 'bold': True}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'play'})
        if video:
            script=video.find('script', text=lambda x: 'jwplayer' in str(x))
            if script:
                sources=quotes(script.string.replace(' ',''),'sources:[{','}],')
                lines=str(sources).split(',')
                for i in range(len(lines)):
                    line=lines[i]
                    if 'file:"' in line:

                        label=quotes(lines[i+1],'label:"', '"')
                        href= URL(quotes(line, 'file:"', '"'))
                        self.add_video(label, href)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for tag_container in _iter(soup.find_all('div', {'class': 'ubox-addedby'})):
            psp(tag_container)
            href =tag_container.find('a')
            if href:
                psp(href)
                self.add_tag(collect_string(href), URL(href.attrs['href']+'videos/', base_url=url), style={'color': 'blue'})

        for tag_container in _iter(soup.find_all('div', {'class': 'ubox-btn'})):
            for href in _iter(tag_container.find_all('a')):
                psp(href)
                self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
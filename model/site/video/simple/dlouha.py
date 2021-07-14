# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class DlouhaSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('dlouha-videa.cz/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_Recent=URL('https://www.dlouha-videa.cz/'),
                    Videos_Most_Viewed=URL('https://www.dlouha-videa.cz/page/1/views/week/'))

        view.add_start_button(picture_filename='model/site/resource/dlouha.png',
                              url=URL("https://www.dlouha-videa.cz/", test_string='porno'),
                              menu_items=menu_items)

    def get_shrink_name(self):
        return 'DV'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'id':'archive'})
        if container:
            # pretty(container)
            for thumbnail in _iter(soup.find_all('div', {'class': 'entry'})):
                # pretty(thumbnail)
                href=thumbnail.find('a',href=True, title=True)
                if href:
                    xref = URL(href.attrs['href'], base_url=url)
                    description = href.attrs['title']

                    # thumb_file = thumbnail.img.attrs['src']
                    # channel_img = thumbnail.find('img', {'class': "img-responsive"})
                    # thumb_file = thumb_file if channel_img is None else channel_img.attrs['src']

                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                    duration = thumbnail.find('span', {'class': "duration"})
                    dur_time = '' if duration is None else str(duration.string)

                    quality = thumbnail.find('span', {'class': "hdlogo"})
                    qual = '' if quality is None else "HD"

                    self.add_thumb(thumb_url=thumb_url, href=xref, popup=description,
                                               labels=[{'text': dur_time, 'align': 'top right'},
                                                       {'text': qual, 'align': 'top left'},
                                                       {'text': description, 'align': 'bottom center'}])


    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('ul',{'class':'simple-list--channels'})
        if container:
            for channel in _iter(container.find_all('a',href=True, title=True)):
                self.add_tag(str(channel.attrs['title']),URL(channel.attrs['href']))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'wp-pagenavi'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video')
        if video:
            # pretty(video)
            for source in _iter(video.find_all('source')):
                self.add_video('default', URL(source.attrs['src'], base_url=url))


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'id':'categories'})
        if container:
            # pretty(container)

            for href in _iter(container.find_all('a',href=lambda x: '/pornoherecky/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style=dict(color='blue'))

            for href in _iter(container.find_all('a',href=lambda x: '/porno-zdarma/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))

            for href in _iter(container.find_all('a',href=lambda x: '/tag/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))



if __name__ == "__main__":
    pass

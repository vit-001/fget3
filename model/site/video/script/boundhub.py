# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class BoundhubSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('boundhub.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Latest=URL('https://www.boundhub.com/latest-updates/'),
                        TopRated=URL('https://www.boundhub.com/top-rated/'),
                        MostViewed=URL('https://www.boundhub.com/most-popular/'),
                        )

        view.add_start_button(picture_filename='model/site/resource/boundhub.png',
                              menu_items=menu_items,
                              url=URL("https://www.boundhub.com/latest-updates/", test_string='Porn'))

    def get_shrink_name(self):
        return 'BH'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for container in soup.find_all('div',{'class':'list-videos'}):
            for thumbnail in _iter(container.find_all('div',{'class':'item'})):
                # pretty(thumbnail)
                xref=thumbnail.find('a')
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    img=xref.find('img')
                    description = img.attrs['alt']
                    thumb_url = URL(img.attrs.get('data-original',thumbnail.img.attrs.get('src')), base_url=url)

                    duration = thumbnail.find('div', {'class': "duration"})
                    dur_time = '' if not duration else collect_string(duration)

                    quality = thumbnail.find('span', {'class': "flag-hd"})
                    qual = '' if quality is None else "HD"

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'},
                                           {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'box tags-cloud'})
        if container:
            pretty(container)

        # if tags is not None:
            for tag in container.find_all('a'):
                self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pagination-holder'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video:
            script=video.find('script', text=lambda x: 'flashvars' in str(x))
            if script:
                t1=quotes(script.string.replace(' ',''),"video_url:'","'")
                self.add_video('default', URL(t1, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info_block=soup.find('div', {'class': 'info'})

        for tag in _iter(info_block.find_all('a')):
            # pretty(tag)
            self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
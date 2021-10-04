# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class KatestubeSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('katestube.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Best=URL('https://www.katestube.com/top-rated/'),
                        Latest=URL('https://www.katestube.com/latest-updates/'),
                        Popular=URL('https://www.katestube.com/most-popular/'),
                        Chanels=URL('https://www.katestube.com/channels/'),
                        Categories=URL('https://www.katestube.com/categories/alphabetical/'))

        view.add_start_button(picture_filename='model/site/resource/katestube.png',
                              menu_items=menu_items,
                              url=URL("https://www.katestube.com/latest-updates/", test_string='Kate\'s'))

    def get_shrink_name(self):
        return 'PO8'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'class':'thumbs-list'})
        # pretty(container)
        if container:
            for thumbnail in _iter(container.find_all('div',{'class':'thumb'})):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a')
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    description = thumbnail.img.attrs.get('alt')
                    thumb_url = URL(thumbnail.img.attrs.get('data-original',thumbnail.img.attrs.get('src')), base_url=url)
                    # psp(thumb_url.get())

                    duration = thumbnail.find('span', {'class': "length"})
                    dur_time = '' if duration is None else collect_string(duration)

                    quality = thumbnail.find('span', {'class': "hd"})
                    qual = '' if quality is None else str(quality.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'},
                                           {'text': qual, 'align': 'top left', 'bold': True}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pager'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video is not None:
            script=video.find('script', text=lambda x: 'video_url:' in str(x))
            if script:
                data = str(script.string).replace(' ', '').replace('\\', '')
                # psp(data)
                mp4=quotes(data,"video_url:'","'")
                self.add_video('DEFAULT', URL(mp4, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        models=soup.find('div',{'class':'models'})
        if models:
            for item in _iter(models.find_all('a', href=True)):
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='red'))

        container = soup.find('div', {'class': 'block-more'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))

        container = soup.find('div', {'class': 'player-tags'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))




        categories=soup.find('div',{'class':'full-category'})
        if categories:
            # pretty(categories)
            for xref in _iter(categories.find_all('a',href=lambda x: not 'javascript' in str(x))):
                # psp(xref)
                href=xref.attrs.get('href','')
                self.add_tag(collect_string(xref), URL(href, base_url=url))



if __name__ == "__main__":
    pass
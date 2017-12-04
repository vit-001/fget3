# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PorntubeSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('porntube.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                        Latest=URL('http://collectionofbestporn.com/most-recent*'),
                        TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                        MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                        Categories=URL('http://collectionofbestporn.com/channels/'),
                        Longest=URL('http://collectionofbestporn.com/longest*'))

        view.add_start_button(picture_filename='model/site/resource/collectionofbestporn.png',
                              menu_items=menu_items,
                              url=URL("https://www.porntube.com/videos?sort=date*", test_string='Movies'))

    def get_shrink_name(self):
        return 'PT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        i=0
        for containrer in _iter(soup.find_all('div',{'class':'video_list'})):

            i+=1
            for thumbnail in _iter(containrer.find_all('div', {'class': 'thumb_video'})):
                # pretty(thumbnail)
                href = URL(thumbnail.a.attrs['href'], base_url=url, load_method='SELENIUM')
                description = thumbnail.a.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['data-master'], base_url=url)

                duration = thumbnail.find('span', {'class': "time"})
                dur_time = '' if duration is None else str(duration.string)

                quality = thumbnail.find('span', {'class': "quality"})
                qual = '' if quality is None else str(quality.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'},
                                       {'text': qual, 'align': 'top left', 'bold': True}])

        psp(i)

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('ul', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video')
        if video is not None:
            pretty(video)
            for source in _iter(video.find_all('source')):
                self.add_video(source.attrs['data-res'], URL(source.attrs['src'], base_url=url))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for tag_container in _iter(soup.find_all('div', {'class': 'tags-container'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
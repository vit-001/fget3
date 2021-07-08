# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class SextubeNlSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('sextube.nl/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(New=URL('http://www.sextube.nl/videos/nieuw*'),
                    Videos_Top_Rated=URL('http://www.sextube.nl/videos/hoog-gewaardeerd*'),
                    Popular=URL('http://www.sextube.nl/videos/populair*'),
                    HD=URL('http://www.sextube.nl/videos/hd*'))

        view.add_start_button(picture_filename='model/site/resource/sextube_nl.png',
                              menu_items=menu_items,
                              url=URL("http://www.sextube.nl/videos/nieuw*"))

    def get_shrink_name(self):
        return 'NL'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class':'videos-list'})
        if container:
            for article in _iter(container.find_all('article')):
                # pretty(article)
                thumbnail=article.find('a')
                href = URL(thumbnail.attrs['href'], base_url=url)

                img=thumbnail.find('img')
                if img:
                    thumb_file=img.attrs.get('data-src',img.attrs.get('src'))
                    thumb_url = URL(thumb_file, base_url=url)

                    label = thumbnail.attrs['title']

                    duration = thumbnail.find('div',{'class':'duration'})
                    dur_time = '' if duration is None else str(duration.string).strip()

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           # {'text': hd, 'align': 'top left'},
                                           {'text':label, 'align':'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('section',{'class':'categories'})
        if container:
            for category in _iter(container.find_all('a',href=True)):
                # psp(category.prettify())
                label=category.find('span',{'class':'highlight'})

                self.add_tag(label.string, URL(category.attrs['href'],base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination2'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'video-player'})
        if container:
            # pretty(container)
            source=container.find('source', src=True)
            if source:
                self.add_video('default',URL(source.attrs['src']))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'tags'})
        if container:
            for tag in container.find_all('a',href=True,title=True):
                self.add_tag(tag.attrs['title'],URL(tag.attrs['href'],base_url=url))

if __name__ == "__main__":
    pass

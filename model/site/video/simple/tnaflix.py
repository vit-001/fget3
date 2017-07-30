# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class TnaflixSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('tnaflix.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(TopRated=URL('https://www.tnaflix.com/toprated/?d=all&period=all*'),
                        MostRecent=URL('https://www.tnaflix.com/new/?d=all&period=all*'),
                        Medium_3to10min=URL('https://www.tnaflix.com/new/?d=medium&period=all*'),
                        Short_1to3min=URL('https://www.tnaflix.com/new/?d=short&period=all*'),
                        FullLenght_over30min=URL('https://www.tnaflix.com/new/?d=full&period=all*'),
                        Popular=URL('https://www.tnaflix.com/popular/?d=all&period=all*'),
                        Categories=URL('https://www.tnaflix.com/categories*'),
                        Channels=URL('https://www.tnaflix.com/channels/all/most-viewed/1*'),
                        Long_10to30min=URL('https://www.tnaflix.com/new/?d=long&period=all*'))

        view.add_start_button(picture_filename='model/site/resource/tnaflix.png',
                              menu_items=menu_items,
                              url=URL("https://www.tnaflix.com/new/?d=all&period=all", test_string='Porn'))

    def get_shrink_name(self):
        return 'TF'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('ul',{'class':['nThumbsList','catsList','channelsList']})):
            # psp('cont')
            for thumbnail in _iter(container.find_all('li')):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a')
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    description = xref.img.attrs['alt']
                    thumb_addr=thumbnail.img.attrs.get('data-original',thumbnail.img.attrs['src'])
                    thumb_url = URL(thumb_addr, base_url=url)

                    duration = thumbnail.find('div', {'class': ["videoDuration",'vidcountSp']})
                    dur_time = collect_string(duration) if duration else ''

                    quality = thumbnail.find('div', {'class': "hdIcon"})
                    qual = collect_string(quality) if quality else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'},
                                           {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        super().parse_others(soup, url)

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('ul', {'class': 'ordered-facets'})
        if tags_container:
            # psp(tags_container.prettify())
            for tag in _iter(tags_container.find_all('a',href=True)):
                # psp(tag.prettify())
                label=str(tag.attrs.get('title', tag.attrs['href'])).strip('\n/ ')
                self.add_tag(label, URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'navigation'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div',{'itemprop':'video'})
        if video:
            # psp(video.prettify())
            content_url=video.find('meta', {'itemprop':'contentUrl'})
            # psp(content_url)
            self.add_video('DEFAULT', URL(content_url.attrs['content'], base_url=url))

            self.title_meta=video.find('h1',{'itemprop':'name'})

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        if self.title_meta:
            # psp(self.title_meta)
            return self.title_meta.string
        else:
            return super().parse_video_title(soup, url)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for tag_container in _iter(soup.find_all('div', {'class': '_video_info'})):
            for href in _iter(tag_container.find_all('a')):
                # psp(href)
                self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
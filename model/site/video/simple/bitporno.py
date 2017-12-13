# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, pretty, psp, collect_string_to_array

import json

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class BitpornoSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('bitporno.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                        Latest=URL('http://collectionofbestporn.com/most-recent*'),
                        TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                        MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                        Categories=URL('http://collectionofbestporn.com/channels/'),
                        Longest=URL('http://collectionofbestporn.com/longest*'))

        view.add_start_button(picture_filename='model/site/resource/bitporno.png',
                              menu_items=menu_items,
                              url=URL("https://www.bitporno.com/", test_string='Bitporno'))

    def get_shrink_name(self):
        return 'BP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'square_entry'})):
            # pretty(thumbnail)

            quality = thumbnail.find('div', {'class': "thumbnail-hd"})
            qual = str(quality.string) if quality else ''

            href = URL(thumbnail.a.attrs['href'], base_url=url)
            if qual:
                description = collect_string_to_array(thumbnail)[1]
            else:
                description = collect_string_to_array(thumbnail)[0]

            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

            duration = thumbnail.find('span', {'class': "time"})
            dur_time = '' if duration is None else str(duration.string)


            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                           labels=[{'text': dur_time, 'align': 'top right'},
                                   {'text': description, 'align': 'bottom center'},
                                   {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'class':'video_results2'})
        pages=set()
        if container:
            for page in _iter(container.find_all('a', {'href': True, "class":'pages'})):
                if page.string and str(page.string).strip().isdigit():
                    label=page.string.strip()
                    if label not in pages:
                        self.add_page(label, URL(page.attrs['href'], base_url=url))
                        pages.add(label)
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'class':'video'})
        if container:
            pretty(container)
            script=container.find('script')
            if script:
                psp(script.string)
                quot=quotes(script.string,'.setup(',');').replace(' ','').replace('\\','')
                psp(quot)
                sources=quotes(quot,'"sources":',']')+']'
                psp(sources)
                try:
                    js=json.loads(sources)

                    self.add_video(js[0]['label'], URL(js[0]['file'], base_url=url))
                except TypeError:
                    print('Not found')


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for tag_container in _iter(soup.find_all('div', {'class': 'tags-container'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
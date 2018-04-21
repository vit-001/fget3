# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter, pretty, collect_string
from data_format.fl_data import FLData
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser


class PornstreamsSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornstreams.eu/')

    @staticmethod
    def create_start_button(view: ViewManagerFromModelInterface):
        menu_items = dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                          Latest=URL('http://collectionofbestporn.com/most-recent*'),
                          TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                          MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                          Categories=URL('http://collectionofbestporn.com/channels/'),
                          Longest=URL('http://collectionofbestporn.com/longest*'))

        view.add_start_button(picture_filename='model/site/resource/pornstream.png',
                              menu_items=menu_items,
                              url=URL("http://pornstreams.eu/", test_string='Porn'))

    def get_shrink_name(self):
        return 'DT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for containrer in _iter(soup.find_all('div', {'class': ['article-container']})):
            # pretty(containrer)
            for thumbnail in _iter(containrer.find_all('article', {'class': 'has-post-thumbnail'})):
                # pretty(thumbnail)
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                description = thumbnail.a.attrs['title']
                thumb_url = URL(thumbnail.a.img.attrs['src'], base_url=url)

                duration = thumbnail.find('em', {'class': "time_thumb"})
                dur_time = collect_string(duration)

                quality = thumbnail.find('i', {'class': "ico_hd"})
                qual = 'HD' if quality else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'},
                                       {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags = soup.find('ul', {'class': 'categories-nav'})
        if tags:
            for tag in tags.find_all('a'):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'wp-pagenavi'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        # containers=soup.find_all('div',{'class':'article-content'})
        # if containers:

            sources=[]
            # for container in containers:
            #     pretty(container)
            for iframe in _iter(soup.find_all('iframe')):

                pretty(iframe)
                src=iframe.attrs['src']
                print(src)
                sources.append(src)

            print(sources)
            if len(sources)>0:
                source_file = URL(sources[-1], load_method='SELENIUM')
                filedata = FLData(source_file, '')

                self._result_type = 'video'
                self.model.loader.start_load_file(filedata, self.continue_parse_video)

    def continue_parse_video(self, fldata: FLData):
        soup = BeautifulSoup(fldata.text, "lxml")
        # pretty(soup)
        container = soup.find('video')
        pretty(container)
        if container:
            self.add_video('Standart', URL(container.attrs['src'], base_url=fldata.url))
            for source in _iter(container.find_all('source')):
                # pretty(source)
                self.add_video(source.attrs['data-res'], URL(source.attrs['src'], base_url=fldata.url))
            # self.set_default_video(-1)
        #
        # self.parse_video_tags(soup,fldata.url)
            self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for tag_container in _iter(soup.find_all('span', {'class': 'cat-links'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})
        for tag_container in _iter(soup.find_all('span', {'class': 'tag-links'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass

    # http://1-957-45-19.b.cdn13.com/mp4_lq/4082638.mp4?cdn_hash=b6f0244b9297656271fcfea1f2fb420f&cdn_creation_time=1512896887&cdn_ttl=3600&cdn_net=80.249.0.0.16&cdn_bw=75000&cdn_bw_fs=713750
    # http://1-96-45-19.b.cdn13.com/mp4_hq/4082638.mp4?cdn_hash=57a2bb3509089ee00f7e816c04748705&cdn_creation_time=1512896887&cdn_ttl=3600&cdn_net=80.249.0.0.16&cdn_bw=233454&cdn_bw_fs=2221708

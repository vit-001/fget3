# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class FapmeifyoucanSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('fapmeifyoucan.net/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/fapmeifyoucan.png',
                              # menu_items=menu_items,
                              url=URL("https://fapmeifyoucan.net/video", test_string='porn'))

    def get_shrink_name(self):
        return 'FM'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'row-small-videos'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'block-video-preview'})):
                try:
                    # psp(thumbnail.prettify())
                    img=thumbnail.find('img', {'alt':True, 'data-src':True} )

                    label=img.attrs['alt']
                    img_url=img.attrs.get('data-src')
                    thumb_url = URL(img_url, base_url=url)

                    xref=thumbnail.find('a',href=True)
                    href = URL(xref.attrs['href'], base_url=url)

                    info=thumbnail.find('div', {'class':'video-information'})
                    dur_time =quotes(collect_string(info),'duration:','view:')

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text':label, 'align':'bottom center'}])
                except AttributeError as e:
                    print(e.__repr__())

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('nav',{'class':'menu-inner2'})
        if container:
            # psp(container.prettify())
            for item in _iter(container.find_all('li',{'class':'cat-item'})):
                # psp(item)
                tag=item.find('a')
                if tag:
                    # psp(tag)
                    self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'navigation'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'class': 'video-player'})
        if video:
            # pretty(video)
            source=video.find('source', src=True)
            # pretty(url)
            if source:
                self.add_video(source.attrs.get('type', 'default'), URL(source.attrs['src']))

    def add_tags(self, soup: BeautifulSoup, url: URL, div_class: str, color=''):
        container = soup.find('div', {'class': div_class})
        # pretty(container)
        if container:
            for xref in _iter(container.find_all('a', href=True)):
                # psp(xref)
                href = xref.attrs.get('href')
                s = dict(color=color)
                self.add_tag(collect_string(xref), URL(href, base_url=url), style=s)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        self.add_tags(soup, url, 'studio', 'blue')
        self.add_tags(soup,url,'actos','red')
        self.add_tags(soup, url, 'tags')
        #
        #
        # container=soup.find('div',{'class':'tags'})
        # # pretty(container)
        # if container:
        #     for xref in _iter(container.find_all('a', href=lambda x: '/tag/' in str(x))):
        #         # psp(xref)
        #         href = xref.attrs.get('href', '')
        #         self.add_tag(collect_string(xref), URL(href, base_url=url))

            # if models:
            #     # pretty(models)

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

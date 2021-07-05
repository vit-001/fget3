# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornoneSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornone.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
                    Latest_Video=URL('https://pornone.com/newest/'),
                    Most_Viewed=URL('https://pornone.com/views/'),
                    Longest_Video=URL('https://pornone.com/longest/'),
                    HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/pornone.png',
                              menu_items=menu_items,
                              url=URL("https://pornone.com/newest/"))

    def get_shrink_name(self):
        return 'VP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class','thumblist videos'})
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'video'})):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('span', {'class': 'time'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_img = thumbnail.find('span', {'class': 'hd-marker '})
                hd = 'HD' if hd_img else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'categories-list'})
        if container:
            # psp(container.prettify())
            for tag in container.find_all('a'):
                self.add_tag(tag.attrs['alt'], URL(tag.attrs['href'], base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pages'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'class': 'video-js'})
        if video is not None:
            for source in _iter(video.find_all('source')):
                if 'http' in source.attrs.get('src',''):
                    self.add_video(source.attrs['label'], URL(source.attrs['src']))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info=soup.find('div',{'class':'video-info'})
        if info:
            # psp(info.prettify())
            for xref in _iter(info.find_all('a',href=lambda x: not 'javascript' in str(x))):
                # psp(xref)
                href=xref.attrs.get('href','')
                if '/user/' in href:
                    self.add_tag(quotes(href,'/user/','/'),URL(href.replace('/user/','/submitted/'),base_url=url), style={'color':'blue'})
                elif '#' not in href:
                    self.add_tag(collect_string(xref), URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        psp(title)
        return title


if __name__ == "__main__":
    pass

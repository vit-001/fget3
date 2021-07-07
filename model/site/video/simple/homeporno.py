# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class HomepornoSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('homeporno.info/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/homeporno.png',
                              # menu_items=menu_items,
                              url=URL("http://homeporno.info/porno-onlain/", test_string='порно'))

    def get_shrink_name(self):
        return 'HP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'id':'dle-content'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('div', {'class': 'th-item'})):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img=thumbnail.find('img',alt=True, src=True)
                if img:
                    # img_url=img.attrs.get('src')
                    thumb_url = URL(img.attrs.get('src'), base_url=url)

                    # title_tag = thumbnail.find('div', {'class': 'th-title'})
                    label = img.attrs.get('alt')

                    duration = thumbnail.find('div', {'class': 'th-time'})
                    dur_time = '' if duration is None else collect_string(duration)
                    #
                    # hd_tag = thumbnail.find('div', {'class': 't-hd'})
                    # if hd_tag is None:
                    #     hd_tag = thumbnail.find('span', {'class': 'hdthumb'})
                    # hd = '' if hd_tag is None else collect_string(hd_tag)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           # {'text': count, 'align': 'top right'},
                                           {'text':label, 'align':'bottom center'}])

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
        video = soup.find('div', {'class': 'player-box'})
        if video:
            # psp(video)
            script = video.find('script', text=lambda x: 'file:' in str(x))
            if script:
                data = str(script.string).replace(' ', '').replace('\\', '')
                # psp(data)
                mp4 = quotes(data, 'file:"', '"')
                self.add_video('DEFAULT', URL(mp4, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('div', {'class':'vp-tags'})):
            # pretty(container)
            for xref in _iter(container.find_all('a')):
                # psp(xref)
                href=xref.attrs.get('href','')
                self.add_tag(collect_string(xref), URL(href, base_url=url))


    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass

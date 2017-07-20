# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PervertslutSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pervertslut.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Categories=URL('http://pervertslut.com/categories/'),
                    Latest=URL('http://pervertslut.com/latest-updates/'),
                    TopRated=URL('http://pervertslut.com/top-rated/'),
                    MostViewed=URL('http://pervertslut.com/most-popular/'))

        view.add_start_button(picture_filename='model/site/resource/pervertslut.png',
                              menu_items=menu_items,
                              url=URL("http://pervertslut.com/latest-updates/", test_string='porn'))

    def get_shrink_name(self):
        return 'PL'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'item'})):
            # psp(thumbnail.prettify())
            xref=thumbnail.find('a')
            if xref:
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('div', {'class': 'duration-overlay'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_span = thumbnail.find('span', {'class': 'hd'})
                hd = '' if hd_span is None else str(hd_span.string).strip()

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'list-categories'})
        if container:
            for xref in _iter(container.find_all('a', {'class':'item'})):
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(xref.img.attrs['src'], base_url=url)
                label = xref.img.attrs.get('alt', '')

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': label, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'sidebar'})
        if tags_container:
            for tag in _iter(tags_container.find_all('a',{'href':lambda x: '/categories/' in x})):
                self.add_tag(collect_string(tag).rstrip('.0123456789'), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination-holder'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video is not None:
            # psp(video.prettify())
            script=video.find('script', text=lambda x: 'video_url:' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')#.replace('\t', '').replace('\n', '')
                # psp(data)
                mp4=quotes(data,"video_url:'","'")
                self.add_video('DEFAULT', URL(mp4, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'info'})
        if container:
            for xref in _iter(container.find_all('a')):
                href=URL(xref.attrs['href'],base_url=url)
                self.add_tag(str(xref.string),href)

if __name__ == "__main__":
    pass

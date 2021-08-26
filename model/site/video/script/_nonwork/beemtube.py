# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class BeemtubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('beemtube.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_Most_Recsent=URL('http://beemtube.com/most-recent/'),
                    Videos_Most_Viewed=URL('http://beemtube.com/most-viewed/'),
                    Videos_Medium_5to20m=URL('http://beemtube.com/duration/medium/'),
                    Videos_Top_Rated=URL('http://beemtube.com/top-rated/'),
                    Videos_Long_20plus=URL('http://beemtube.com/duration/long/'),
                    Videos_Short=URL('http://beemtube.com/duration/short/'),
                    Channels=URL('http://beemtube.com/channels/'),
                    Categories=URL('http://beemtube.com/categories/')
                    )

        view.add_start_button(picture_filename='model/site/resource/beemtube.png',
                              menu_items=menu_items,
                              url=URL("http://beemtube.com/most-recent/"))

    def get_shrink_name(self):
        return 'BMT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'videos'})
        if contents:
            for thumbnail in _iter(contents.find_all('div', {'class': 'content'})):
                psp(thumbnail.prettify())
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['data-src'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('div', {'class': 'duration'})
                dur_time = '' if duration is None else str(duration.string)

                hd_span = thumbnail.find('span', {'class': 'hd_video'})
                hd = 'HD' if hd_span else ''

                count_em=thumbnail.find('em')
                count = '' if count_em is None else str(count_em.string)


                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class','videos'})
        if contents:
            for thumbnail in _iter(contents.find_all('a', {'class': 'partners'})):
                href = URL(thumbnail.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                title_span = thumbnail.find('span', {'class': 'title'})
                title = '' if title_span is None else str(title_span.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=title,
                               labels=[{'text':title, 'align':'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'id': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div',{'class':'contents'})
        if contents:
            script=contents.find('script',text=lambda x: 'beemPlayer' in str(x))
            if script:
                # psp(script.prettify())
                video_url=URL(quotes(str(script.text),'file:',',').strip(' "'),referer=url)
                self.add_video('default',video_url)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for info_holder in _iter(soup.find_all('div',{'class':'info_holder'})):
            # psp(info_holder.prettify())
            for xref in _iter(info_holder.find_all('a', href=True)):
                # psp(xref)
                href=str(xref.attrs['href'])
                if '/profiles/' in href:
                    self.add_tag(xref.string, URL(href.replace('.html','/videos/')), style=dict(color='blue'))
                if '/category/' in href or '/search-porn/' in href or '/channel/' in href:
                    self.add_tag(xref.string, URL(href))

if __name__ == "__main__":
    pass

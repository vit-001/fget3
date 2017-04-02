# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class VpornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('vporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        menu_items=dict(Top_Rated_Video=URL('http://www.vporn.com/rating'),
                    Latest_Video=URL('http://www.vporn.com/newest'),
                    Longest_Video=URL('https://www.vporn.com/longest/'),
                    HD_video=URL('http://www.vporn.com/newest/hd'))

        view.add_start_button(picture_filename='model/site/resource/vporn.png',
                              menu_items=menu_items,
                              url=URL("http://www.vporn.com/newest/"))

    def get_shrink_name(self):
        return 'VP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class','thumblist'})
        if contents:
            for thumbnail in _iter(contents.find_all('div', {'class': 'bx'})):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('span', {'class': 'time'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_img = duration.find('img', {'alt': 'HD Video'})
                hd = 'HD' if hd_img else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagerwrap'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'video_panel'})
        if video is not None:
            script=video.find('script', text=lambda x: 'var flashvars' in str(x))
            if script is not None:
                script=str(script.string).partition('flashvars.')[2]
                while script:
                    parts=script.partition(';')
                    pair=parts[0].partition('=')
                    script=script.partition('flashvars.')[2]

                    if pair[0].startswith('videoUrl'):
                        label=pair[0].partition('videoUrl')[2]
                        href=pair[2].strip('" ')

                        if href.startswith('http://') or href.startswith('https://'):
                            self.add_video(label, URL(href))
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        details=soup.find('div',{'class':'video-details'})
        if details:
            for xref in _iter(details.find_all('a',  {'class':['cwrap','tags']}, href=True)):
                # psp(xref)
                href=str(xref.attrs['href'])
                color = None
                if '/user/' in href:
                    href=href.replace('/user/','/submitted/')
                    color = 'blue'

                self.add_tag(xref.string, URL(href,base_url=url), style=dict(color=color))

if __name__ == "__main__":
    pass

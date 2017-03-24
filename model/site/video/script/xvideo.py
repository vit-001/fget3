# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class XvideoSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('xvideos.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Best_Recent=URL('http://www.pornoxo.com/'),
                    Most_popular=URL('http://www.pornoxo.com/most-viewed/page1.html?s*'),
                    Latest=URL('http://www.pornoxo.com/newest/page1.html?s*'),
                    Top_Rated=URL('http://www.pornoxo.com/top-rated/page1.html?s*'),
                    Longest=URL('http://www.pornoxo.com/longest/page1.html?s*'))

        view.add_start_button(picture_filename='model/site/resource/xvideos.gif',
                              menu_items=menu_items,
                              url=URL("http://www.xvideos.com/", test_string='XVIDEOS.COM'))

    def get_shrink_name(self):
        return 'XV'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'thumb-block '})):
            href=thumbnail.find('a', title=True, href=lambda x: str(x).startswith('/video'))
            if href:
                xref_url = URL(href.attrs['href'], base_url=url)
                label = href.attrs['title']

                script=thumbnail.script.string
                thumb_url = URL(quotes(script,'src="','"'), base_url=url)

                metadata=thumbnail.find('p', {'class','metadata'})
                duration = metadata.find('strong')
                dur_time = '' if duration is None else str(duration.string)

                hd_span = thumbnail.find('span', {'class': 'video-hd-mark'})
                hd = '' if hd_span is None else str(hd_span.string)

                self.add_thumb(thumb_url=thumb_url, href=xref_url, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'left-menu-box-wrapper'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a',{'href':lambda x: '/videos/' in x})):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'video-player-bg'})
        if video is not None:
            psp(video.prettify())
            script=video.find('script', text=lambda x: 'HTML5Player' in str(x))
            if script is not None:
                psp(script.prettify())
                data = str(script.string).replace(' ', '').replace('\t', '').replace('\n', '')
                if 'sources:' in data:
                    sources=quotes(data,'sources:[{','}]').split('},{')
                    for item in sources:
                        file = quotes(item, 'file:"', '"')
                        label=quotes(item,'label:"','"')
                        self.add_video(label, URL(file, base_url=url))
                elif "filefallback':" in data:
                    file=quotes(data,'filefallback\':"','"')
                    self.add_video('DEFAULT', URL(file, base_url=url))

                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # adding "user" to video
        user = soup.find('div', {'class': 'user-card'})
        if user is not None:
            href = user.find('a').attrs['href']
            username = user.find('span', {'class': 'name'}).string
            self.add_tag(username, URL(href, base_url=url), style=dict(color='blue'))

        # adding tags to video
        for item in _iter(soup.find_all('div', {'class': 'content-tags'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))

if __name__ == "__main__":
    pass

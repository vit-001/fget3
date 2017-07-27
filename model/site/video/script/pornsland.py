# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornslandSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornsland.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Channels=URL('http://pornsland.com/video-channels*'),
                    Pornstars=URL('http://pornsland.com/pornstars*'),
                    Latest=URL('http://pornsland.com/recent-porns*'),
                    MostLiked=URL('http://pornsland.com/most-liked-porns*'),
                    MostViewed=URL('http://pornsland.com/most-viewed-porns*'),
                    Categories=URL('http://pornsland.com/video-categories*'))

        view.add_start_button(picture_filename='model/site/resource/pornsland.png',
                              menu_items=menu_items,
                              url=URL("http://pornsland.com/recent-porns*", test_string='Porns'))

    def get_shrink_name(self):
        return 'PL'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': ['video','category','pornstar','serie']})):
            # psp(thumbnail.prettify())
            xref=thumbnail.find('a')
            if xref:
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['data-original'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_span = thumbnail.find('span', {'class': 'hd'})
                hd = '' if hd_span is None else str(hd_span.string).strip()

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'left-menu-box-wrapper'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a',{'href':lambda x: '/videos/' in x})):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'my-pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video is not None:
            psp(video.prettify())
            script=video.find('script', text=lambda x: 'playerInstance.setup(' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')#.replace('\t', '').replace('\n', '')
                # psp(data)
                mp4=quotes(data,"file:'","'")
                self.add_video('DEFAULT', URL(mp4, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'extra-detail'})
        # psp(container.prettify())

        for values in _iter(container.find_all('div',{'class':'values'})):
            for xref in _iter(values.find_all('a')):
                # psp(xref)
                href=URL(xref.attrs['href'],base_url=url)
                if href.contain('/pornstar/'):
                    style = dict(color='red')
                else:
                    style = None

                self.add_tag(str(xref.string),href, style=style)

if __name__ == "__main__":
    pass

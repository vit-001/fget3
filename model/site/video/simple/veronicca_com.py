# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from common.util import _iter

from model.site.base_site import BaseSiteParser,ViewFromModelInterface, BeautifulSoup

class VeroniccaComSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('veronicca.com/')

    @staticmethod
    def create_start_button(view:ViewFromModelInterface):
        view.add_start_button(name='veronicca.com',
                              picture_filename='',
                              url=URL("https://www.veronicca.com/videos?o=mr*", test_string='Veronicca'))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in soup.find_all('div', {'class': ['well well-sm hover', 'channelBox']}):
            # psp(thumbnail)
            href = URL(thumbnail.a.attrs['href'], base_url=url)
            description = thumbnail.a.img.attrs['alt']

            thumb_file = thumbnail.img.attrs['src']
            channel_img = thumbnail.find('img', {'class': "img-responsive"})
            thumb_file = thumb_file if channel_img is None else channel_img.attrs['src']

            thumb_url = URL(thumb_file, base_url=url)

            duration = thumbnail.find('div', {'class': "duration"})
            dur_time = '' if duration is None else duration.stripped_strings.__next__()

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text': dur_time, 'align': 'top right'},
                                               {'text': description, 'align': 'bottom center'}])

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get()


if __name__ == "__main__":
    pass
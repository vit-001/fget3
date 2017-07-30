# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class DonfreepornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('donfreeporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/DonFreePorn.jpg',
                              url=URL("http://donfreeporn.com/"))

    def get_shrink_name(self):
        return 'DFP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'post'})):

            href = URL(thumbnail.a.attrs['href'], base_url=url)
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
            label=thumbnail.img.attrs.get('alt','')
            self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                           labels=[{'text':label, 'align':'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class':'wp-pagenavi'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video_container=soup.find('div',id='video')
        if video_container:
            video=video_container.find('video', src=True)
            if video:
                src=str(video.attrs['src'])
                self.add_video('default', URL(src))
                return

            frame=video_container.find('iframe', src=True)
            if frame:
                src=str(frame.attrs['src'])
                code=src.rpartition('embed.php?f=')[2]
                data = {'data':code}

                loader_url=URL('http://donfreeporn.com/wp-content/themes/detube-noedit/Htplugins/Loader.php',
                               method='POST',
                               post_data=data)

                filedata = FLData(loader_url, '')

                self._result_type = 'video'
                self.model.loader.start_load_file(filedata, self.continue_parse_video)

    def continue_parse_video(self, fldata: FLData):
        jdata=json.loads(fldata.text)
        for href, label in zip(jdata['l'],jdata['q']):
            self.add_video(label,URL(href))
        self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        extras=soup.find('div', id='extras')
        if extras:
            # psp(extras.prettify())
            for xref in _iter(extras.find_all('a', href=True)):
                self.add_tag(xref.string,URL(xref.attrs['href']))

if __name__ == "__main__":
    pass

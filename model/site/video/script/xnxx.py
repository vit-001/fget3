# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
from json import loads

from common.util import _iter, quotes, collect_string,psp, pretty
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser


class XnxxSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('xnxx.com/')

    @staticmethod
    def create_start_button(view: ViewManagerFromModelInterface):
        menu_items = dict(BestOf=URL('http://www.xnxx.com/best/'),
                          Newest_Video=URL('http://www.xnxx.com/'),
                          Hot=URL('http://www.xnxx.com/hot/'),
                          MostViewed=URL('http://www.xnxx.com/hits/'),
                          MainPage=URL('http://www.xnxx.com/'),
                          )

        view.add_start_button(picture_filename='model/site/resource/xnxx.png',
                              menu_items=menu_items,
                              url=URL("https://www.xnxx.com/hits*", test_string='Porn'))

    def get_shrink_name(self):
        return 'XNXX'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'mozaique'})
        if container:
            for thumbnail in _iter(container.find_all('div',{'class':'thumb-block'})):
                # pretty(thumbnail)
                try:
                    href = URL(thumbnail.a.attrs['href'], base_url=url)
                    thumb_url = URL(thumbnail.img.attrs['data-src'].replace('THUMBNUM','2'), base_url=url)
                    label = thumbnail.find('a',title=True).attrs['title']

                    duration = thumbnail.find('span', {'class': 'video-duration-mark'})
                    dur_time = collect_string(duration).strip('()') if duration else ''

                    hd_span = thumbnail.find('span', {'class': 'video-hd-mark'})
                    hd = collect_string(hd_span) if hd_span else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except KeyError:
                    pass
                except AttributeError:
                    pass

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'id': 'side-categories'})
        if tags_container is not None:
            script=tags_container.find('script')
            data=script.text.partition('(')[2].rpartition(',')[0]
            try:
                json=loads(data)
                for item in json:
                    self.add_tag(item['label'], URL(item['url'], base_url=url))
            except ValueError:
                print('Thumbs was not recognized')

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'id': 'video-content'})
        if container:
            script = container.find('script', text=lambda x: 'html5player.setVideoUrl' in str(x))
            if script:
                for line in script.text.split(';'):
                    if line.strip().startswith('html5player.setVideoUrl'):
                        label=quotes(line,'setVideoUrl','(')
                        video_url=URL(quotes(line,"('","')"),base_url=url)
                        self.add_video(label, video_url)
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'video-tags'})
        if container:
            for href in _iter(container.find_all('a', href=True)):
                xref = href.attrs['href']
                self.add_tag(str(href.string), URL(xref, base_url=url))


if __name__ == "__main__":
    pass

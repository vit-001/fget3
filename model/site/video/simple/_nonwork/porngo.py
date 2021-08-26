# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PorngoSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('porngo.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(TopRatedAll=URL('https://www.porngo.com/top-rated/'),
                        Latest=URL('https://www.porngo.com/latest-updates/'),
                        TopRatedMonth=URL('https://www.porngo.com/top-rated/month/'),
                        MostViewedAll=URL('https://www.porngo.com/most-popular/'),
                        MostViewedMonth=URL('https://www.porngo.com/most-popular/month/'),
                        )

        view.add_start_button(picture_filename='model/site/resource/porngo.svg',
                              menu_items=menu_items,
                              url=URL("https://www.porngo.com/latest-updates/", test_string='Porn'))

    def get_shrink_name(self):
        return 'PG'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'class':'thumbs-list'})
        # pretty(container)
        if container:
            for thumbnail in _iter(container.find_all('div',{'class':'item'})):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a')
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    img=xref.find('img')
                    description = img.attrs['alt']
                    thumb_url = URL(img.attrs.get('data-src',thumbnail.img.attrs.get('src')), base_url=url)
                    # psp(thumb_url.get())

                    duration = thumbnail.find('span', {'class': "thumb__duration"})
                    dur_time = '' if duration is None else collect_string(duration)

                    quality = thumbnail.find('span', {'class': "thumb__bage"})
                    qual = '' if quality is None else str(quality.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'},
                                           {'text': qual, 'align': 'top left', 'bold': True}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pagination'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('ul', {'class': 'nav-menu underline'})
        if tags_container:
            for tag in _iter(tags_container.find_all('a',href=lambda x: '/categories/' in str(x))):
                xref=tag.attrs['href']
                self.add_tag(collect_string(tag), URL(xref, base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video')
        if video:
            psp(video.prettify())
            for source in _iter(video.find_all('source')):
                # psp(source)
                self.add_video(source.attrs['label'], URL(source.attrs['src'], base_url=url, referer=url))
            # self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'video-links'})

        pretty(container)

        for href in _iter(container.find_all('a',href=lambda x: '/sites/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style={'color': 'red'})

        for href in _iter(container.find_all('a',href=lambda x: '/models/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})

        for href in _iter(container.find_all('a',href=lambda x: '/categories/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))



if __name__ == "__main__":
    pass
# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class VeroniccaComSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('veronicca.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items={
            'Videos most recsent':URL('https://www.veronicca.com/videos?o=mr*'),
            'Videos most viewed': URL('https://www.veronicca.com/videos?o=mv*'),
            'Videos most commented': URL('https://www.veronicca.com/videos?o=md*'),
            'Videos top rated': URL('https://www.veronicca.com/videos?o=tr*'),
            'Videos top favorited': URL('https://www.veronicca.com/videos?o=tf*'),
            'Videos longest': URL('https://www.veronicca.com/videos?o=lg*'),
            'Channels': URL('https://www.veronicca.com/channels*')
        }

        view.add_start_button(picture_filename='model/site/resource/veronicca_com.png',
                              url=URL("https://www.veronicca.com/videos?o=mr*", test_string='Veronicca'),
                              menu_items=menu_items)

    def get_shrink_name(self):
        return 'VER'

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

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags = soup.find('ul', {'class': 'drop2 hidden-xs'})
        if tags:
            for tag in tags.find_all('a'):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup)->BeautifulSoup:
        return soup.find('ul', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'video-container'})
        if video is not None:
            for source in _iter(video.find_all('source')):
                self.add_video(source.attrs['res'], URL(source.attrs['src'], base_url=url))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        user = soup.find('div', {'class': 'pull-left user-container'})
        if user is not None:
            user_strings = [string for string in user.stripped_strings]
            label = '{0} {1}'.format(user_strings[0], user_strings[1])
            href = user.find('a', href=lambda x: '#' not in x)
            self.add_tag(label,
                         URL(href.attrs['href'] + '/videos', base_url=url),
                         style={'color':'blue'}
                        )

        for tag_container in _iter(soup.find_all('div', {'class': 'm-t-10 overflow-hidden'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
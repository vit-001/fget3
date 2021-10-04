# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class MotherlessSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('motherless.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Galleries_Recently_Updated=URL('http://motherless.com/galleries/updated*'),
                    Galleries_Most_Viewed=URL('http://motherless.com/galleries/viewed*'),
                    Galleries_Most_Favorited=URL('http://motherless.com/galleries/favorited*'),
                    Videos_Recent=URL('http://motherless.com/videos/recent*'),
                    Videos_Most_Viewed=URL('http://motherless.com/videos/viewed*'),
                    Videos_Most_Favoritede=URL('http://motherless.com/videos/favorited*'),
                    Videos_Popular=URL('http://motherless.com/videos/popular*'),
                    Videos_Live=URL('http://motherless.com/live/videos*'),
                    Videos_All_Time_Most_Viewed=URL('http://motherless.com/videos/all/viewed*'),
                    Videos_All_Time_Most_Favorited=URL('http://motherless.com/videos/all/favorited*'),
                    Videos_Archived=URL('http://motherless.com/videos/archives*'))

        view.add_start_button(picture_filename='model/site/resource/motherless.png',
                              menu_items=menu_items,
                              url=URL("http://motherless.com/videos/recent?page=1*", test_string='MOTHERLESS.COM'))

    def get_shrink_name(self):
        return 'ML'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for item in _iter(soup.find_all('div', {'class': ['content-inner']})):
            for thumbnail in _iter(item.find_all('div', {'class': 'thumb'})):
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                duration = thumbnail.find('div', {'class': 'caption left'})
                dur_time = '' if duration is None else str(duration.string)

                caption = thumbnail.find('h2', {'class': 'caption title'})
                label = '' if caption is None else str(caption.string)

                user = thumbnail.find('a', {'class': 'caption left'})
                username = '' if user is None else str(user.string)

                if not 'x' in dur_time:
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': username, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags = soup.find('div', {'class': 'dark-menu'})
        if tags is not None:
            for tag in _iter(tags.find_all('a')):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pagination_link'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'id': 'content'})
        if content is not None:
            script = content.find('script', text=lambda x: 'jwplayer(' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, '"file":"', '"')
                self.add_video('DEFAULT', URL(file, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        title=soup.find('h1',{'id':'view_qt5-upload-title'})
        if title:
            return title.string.strip()
        else:
            return 'No title'

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # adding "user" to video
        user = soup.find('div', {'class': 'thumb-member-username'})
        if user is not None:
            href = user.find('a').attrs['href']
            username = href.rpartition('/')[2]

            self.add_tag(username + ' uploads', URL('http://motherless.com/u/' + username + '*'), style=dict(color='blue'))
            self.add_tag(username + ' gals', URL('http://motherless.com/galleries/member/' + username + '*'),style=dict(color='blue'))

        # adding tags to video
        for item in _iter(soup.find_all('div', {'id': 'media-tags-container'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass

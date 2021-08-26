# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornbozzSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornbozz.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Channels=URL('http://www.pornbozz.com/channels/'),
                    Galleries_Recent=URL('http://www.pornbozz.com/photos/'),
                    Galleries_Most_Viewed=URL('http://www.pornbozz.com/photos/most-viewed/'),
                    Galleries_Top_Rated=URL('http://www.pornbozz.com/photos/top-rated/'),
                    Videos_Recent=URL('http://www.pornbozz.com/videos/'),
                    Videos_Most_Viewed=URL('http://www.pornbozz.com/most-viewed/'),
                    Videos_Top_Rated=URL('http://www.pornbozz.com/top-rated/'),
                    Videos_Longest=URL('http://www.pornbozz.com/longest/'))

        view.add_start_button(picture_filename='model/site/resource/pornbozz.png',
                              url=URL("http://www.pornbozz.com/videos/"),
                              menu_items=menu_items)

    def get_shrink_name(self):
        return 'PBZ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'item-inner-col'})):
            xref=thumbnail.a.attrs['href']
            if '/video/' in xref or '/galleries/' in xref:
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                description = thumbnail.a.img.attrs['alt']

                thumb_file = thumbnail.img.attrs['src']
                channel_img = thumbnail.find('img', {'class': "img-responsive"})
                thumb_file = thumb_file if channel_img is None else channel_img.attrs['src']

                thumb_url = URL(thumb_file, base_url=url)

                duration = thumbnail.find('span', {'class': "time"})
                dur_time = '' if duration is None else str(duration.string)

                quality = thumbnail.find('span', {'class': "quality-icon"})
                qual = '' if quality is None else str(quality.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text': dur_time, 'align': 'top right'},
                                                   {'text': qual, 'align': 'top left'},
                                                   {'text': description, 'align': 'bottom center'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'item-inner-col'})):
            href = URL(thumbnail.a.attrs['href'], base_url=url)
            thumb_url = URL(thumbnail.img.attrs['src'])
            description = thumbnail.img.attrs['alt']

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                           labels=[{'text': description, 'align': 'bottom center'}])


    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('ul',{'class':'simple-list--channels'})
        if container:
            for channel in _iter(container.find_all('a',href=True, title=True)):
                self.add_tag(str(channel.attrs['title']),URL(channel.attrs['href']))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('nav',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video')
        if video is not None:
            for source in _iter(video.find_all('source')):
                self.add_video('default', URL(source.attrs['src'], base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        user_container=soup.find('div',{'class':'submitter-container'})
        xref=user_container.find('a',href=True,title=True)
        if user_container:
            username=str(xref.attrs['title'])
            href=str(xref.attrs['href'])
            user_number=href.rstrip('/').rpartition('-')[2]

            self.add_tag(username + ' videos',
                         URL('http://www.pornbozz.com/uploads-by-user/{0}/'.format(user_number)),
                         style={'color': 'blue'})

            self.add_tag(username +  ' photos',
                         URL('http://www.pornbozz.com/uploads-by-user/{0}/?photos=1'.format(user_number)),
                         style={'color': 'blue'})

        for tags_block in _iter(soup.find_all('div',{'class':'tags-block'})):
            for href in _iter(tags_block.find_all('a',href=True)):
                self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        gallery=soup.find('div',{'class':'gallery-block'})
        if gallery:
            for image in _iter(gallery.find_all('img',src=True)):
                image_url=URL(str(image.attrs['src']).replace('/thumbs/','/'))
                filename = image_url.get_path() + image_url.get().rpartition('/')[2]
                self.add_picture(filename, image_url)

    def parse_pictures_tags(self, soup: BeautifulSoup, url: URL):
        self.parse_video_tags(soup,url)

if __name__ == "__main__":
    pass

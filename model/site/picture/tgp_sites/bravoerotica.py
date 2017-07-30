# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter, quotes
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.picture.base_of_tgp import TgpSite


class BravoeroticaSite(TgpSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('bravoerotica.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Movies=URL('http://www.bravoerotica.com/erotic-tube/latest-updates/'),
                        Pics=URL('http://www.bravoerotica.com/'),
                        # LatestUpdates=URL('http://www.tomorrowporn.com/latest_updates.html'),
                    )

        view.add_start_button(picture_filename='model/site/resource/picture/bravoerotica.png',
                              menu_items=menu_items,
                              url=URL("http://www.bravoerotica.com/"))

    def get_shrink_name(self):
        return 'BE '

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_containers = _iter(soup.find_all('li', {'class': 'dropdown'}))
        for tags_container in tags_containers:
            for tag in tags_container.find_all('a', {'href': lambda s: '/st/niches/' in s}):
                # psp(tag.prettify())
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup)->BeautifulSoup:
        return soup.find('div', {'class': ['pages','pg']})

    # def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
    #     return 'BE '+ url.get().partition('bravoerotica.com/')[2].rpartition('.')[0]

    def parse_video_thumbs(self, soup: BeautifulSoup, url: URL):
        thumbs_containers = _iter(soup.find_all('div', {'class': 'video_list'}))
        for thumbs_container in thumbs_containers:
            for thumbnail in _iter(thumbs_container.find_all('a', {'class': ['item']})):
                href = URL(thumbnail.attrs['href'], base_url=url)
                description = thumbnail.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                duration = thumbnail.find('span', {'class': "duration"})
                dur_time = '' if duration is None else str(duration.span.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text': dur_time, 'align': 'top right'},
                                                   {'text': description, 'align': 'bottom center'}])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'class': 'player'})
        if content is not None:
            script = content.find('script', text=lambda x: 'flashvars =' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, "video_url:'", "'")
                self.add_video('DEFAULT', URL(file, base_url=url))

    def get_picture_tag_containers(self, soup:BeautifulSoup)->list:
        crumbles=soup.find('div',{'class':'crumbles'})
        return crumbles.find_all('h1') if crumbles else []


if __name__ == "__main__":
    pass
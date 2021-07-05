# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class Porn0sexSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('porn0sex.online/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Latest=URL('https://www.boundhub.com/latest-updates/'),
                        TopRated=URL('https://www.boundhub.com/top-rated/'),
                        MostViewed=URL('https://www.boundhub.com/most-popular/'),
                        )

        view.add_start_button(picture_filename='model/site/resource/pornosex.png',
                              menu_items=menu_items,
                              url=URL("https://porn0sex.online/",
                                      user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
                                      test_string='Порно'))

    def get_shrink_name(self):
        return 'PS'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        def test(tag:BeautifulSoup):
            if tag.name != 'div':
                return False
            if tag.has_attr('class'):
                if 'ajax-most-recent-videos' in tag.attrs['class'] or 'ajax-common-videos-list' in tag.attrs['class']:
                    return True
            return False

        # for container in soup.find_all('div',{'class':'container p15 ajax-most-recent-videos'}):
        for container in _iter(soup.find_all(test)):
            # pretty(container)
            for thumbnail in _iter(container.find_all('a',{'class':'th-video'})):
                # pretty(thumbnail)
                # xref=thumbnail.find('a')
                # if xref:
                href = URL(thumbnail.attrs['href'], base_url=url)
                img=thumbnail.find('img')
                description = img.attrs['alt']
                thumb_url = URL(img.attrs.get('data-original',thumbnail.img.attrs.get('src')), base_url=url)

                duration = thumbnail.find('span', {'class': "time"})
                dur_time = '' if not duration else collect_string(duration)

                quality = thumbnail.find('span', {'class': "flag-hd"})
                qual = '' if quality is None else "HD"

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'},
                                       {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'cl-content'})
        if container:
            # pretty(container)

        # if tags is not None:
            for tag in container.find_all('a'):
                self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('ul', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        # video = soup.find('div', {'class': 'thr-other'})
        # if video:
        #     pretty(video)
        # script=soup.find('script', text=lambda x: 'flashvars' in str(x))
        # psp(quotes(str(soup).replace(' ',''),'flashvars={','}'))
        flashvars=quotes(str(soup).replace(' ',''),'flashvars={','}')
        if flashvars:
            # psp(flashvars)

            video_url=quotes(flashvars,"video_url:'","'")
            video_url_text=quotes(flashvars,"video_url_text:'","'")

            video_alt_url=quotes(flashvars,"video_alt_url:'","'")
            video_alt_url_text=quotes(flashvars,"video_alt_url_text:'","'")

            self.add_video(video_url_text, URL(video_url, base_url=url))
            self.add_video(video_alt_url_text, URL(video_alt_url, base_url=url))


        # print(video_url)
        # print(video_url_text)
        # print(video_alt_url)
        # psp(video_alt_url_text)

        # if script:
        #     t1=quotes(script.string.replace(' ',''),"video_url:'","'")
        #     self.add_video('default', URL(t1, base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # Обходим ошибки в HTML коде
        # Находим последний правильный DIV
        wrapper=soup.find('div', {'class': 'thrcol p15'})
        if wrapper:
        # Вручную выделяем DIV с категориями
            parts=str(wrapper).partition('<div class="tr-details">')
        # Делаем из него новый суп
            new_soup=BeautifulSoup(parts[1]+parts[2])
        # А дальше все как обычно
            info_block = new_soup.find('div', {'class': 'tr-details'})

            if info_block:
                for tag in _iter(info_block.find_all('a')):
                    self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass
# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class RapelustSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('rapelust.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/rapelust.png',
                              # menu_items=menu_items,
                              url=URL("https://rapelust.com/", test_string='porn'))

    def get_shrink_name(self):
        return 'PA'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('section', {'id':'content'})
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'videoPost'})):
                # pretty(thumbnail)

                # img=thumbnail.find('a', {'class':'post_img'})
                # text=thumbnail.find('div',{'class':'short_post_content'})
                # pretty(img)
                # pretty(text)

                xref=thumbnail.find('a',href=True, title=True)
                href = URL(xref.attrs['href'], base_url=url)
                label=xref.attrs['title']

                img_url=xref.img.attrs.get('src')
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                # label = '' if title_tag is None else collect_string(title_tag)

                duration = thumbnail.find('div', {'class': 'thumbDuration'})
                # if duration is None:
                #     duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('div', {'class': 't-hd'})
                # if hd_tag is None:
                #     hd_tag = thumbnail.find('span', {'class': 'hdthumb'})
                hd = '' if hd_tag is None else collect_string(hd_tag)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    # def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
    #     container=soup.find('nav',{'class':'menu-inner2'})
    #     if container:
    #         # psp(container.prettify())
    #         for item in _iter(container.find_all('li',{'class':'cat-item'})):
    #             # psp(item)
    #             tag=item.find('a')
    #             if tag:
    #                 # psp(tag)
    #                 self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('nav',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'videoBox'})
        if video:
            # pretty(video)
            player=video.find('div',{'class':'flowplayer'})
            # pretty(player)
            sources=player.attrs.get('data-item')
            # psp(sources.replace('\\',''))
            # psp(quotes(sources.replace('\\',''),'"src":"','"'))
            self.add_video('default', URL(quotes(sources.replace('\\',''),'"src":"','"')))


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'videoTags'})
        if container:
            # pretty(container)

            for xref in _iter(container.find_all('a', href=lambda x: '/tag/' in str(x))):
                # psp(xref)
                href = xref.attrs.get('href', '')
                self.add_tag(collect_string(xref), URL(href, base_url=url))

        # if models:
        #     # pretty(models)

        #
        # categories=soup.find('div',{'class':'full-category'})
        # if categories:
        #     # pretty(categories)
        #     for xref in _iter(categories.find_all('a',href=lambda x: not 'javascript' in str(x))):
        #         # psp(xref)
        #         href=xref.attrs.get('href','')
        #         self.add_tag(collect_string(xref), URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass

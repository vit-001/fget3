# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornoaktSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornoakt.click/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/pornoakt.png',
                              # menu_items=menu_items,
                              url=URL("https://pornoakt.click/", test_string='порно'))

    def get_shrink_name(self):
        return 'PA'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'id':'dle-content'})
        # pretty(contents)
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('article', {'class': 'shortstory'})):
                psp(thumbnail.prettify())
                img=thumbnail.find('a', {'class':'post_img'})
                text=thumbnail.find('div',{'class':'short_post_content'})
                # pretty(img)
                # pretty(text)

                xref=text.find('a',href=True, title=True)
                href = URL(xref.attrs['href'], base_url=url)
                label=xref.attrs['title']

                img_url=img.img.attrs.get('src')
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                # label = '' if title_tag is None else collect_string(title_tag)

                duration = img.find('div', {'class': 'video_time'})
                # if duration is None:
                #     duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('div', {'class': 't-hd'})
                if hd_tag is None:
                    hd_tag = thumbnail.find('span', {'class': 'hdthumb'})
                hd = '' if hd_tag is None else collect_string(hd_tag)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('nav',{'class':'menu-inner2'})
        if container:
            # psp(container.prettify())
            for item in _iter(container.find_all('li',{'class':'cat-item'})):
                # psp(item)
                tag=item.find('a')
                if tag:
                    # psp(tag)
                    self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'navigation'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'dlevideoplayer'})
        if video:
            # pretty(video)
            url=video.find('li', {'data-url':True})
            # pretty(url)
            if url:
                self.add_video(url.attrs.get('data-type', 'default'), URL(url.attrs['data-url']))


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'full-info'})
        pretty(container)

        for xref in _iter(container.find_all('a', href=lambda x: '/actors/' in str(x))):
            # psp(xref)
            href = xref.attrs.get('href', '')
            self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='red'))

        for xref in _iter(container.find_all('a', href=lambda x: '/user/' in str(x))):
            # psp(xref)
            href = xref.attrs.get('href', '')+'news/'
            self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='blue'))

        for xref in _iter(container.find_all('a', href=lambda x: not '/tags/' in str(x) and
                                                                 not '/user/' in str(x) and
                                                                 not '/actors/' in str(x) and
                                                                 not '#' in str(x)
                                             )):
            # psp(xref)
            href = xref.attrs.get('href', '')
            self.add_tag(collect_string(xref), URL(href, base_url=url))

        for xref in _iter(container.find_all('a', href=lambda x: '/tags/' in str(x))):
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

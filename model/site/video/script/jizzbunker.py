# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class JizzbunkerSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('jizzbunker.net/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/jizzbunker.png',
                              # menu_items=menu_items,
                              url=URL("https://jizzbunker.net/ru/newest*",test_string='порноролики'))

    def get_shrink_name(self):
        return 'JB'

    def goto_url(self, url: URL, **options):
        url.coockies={'hdsh':'1'}
        super().goto_url(url, **options)

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('ul', {'class','gallery'})
        if contents:
            # psp(contents.prettify())
            for thumbnail in _iter(contents.find_all('figure')):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-original',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                label = xref.attrs.get('title','')

                duration = thumbnail.find('li', {'class': 'dur'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('span', {'class': 'thd'})
                # if hd_tag is None:
                #     hd_tag = thumbnail.find('span', {'class': 'hdthumb'})
                hd = '' if hd_tag is None else 'HD'

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
        return soup.find('ul',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        # pretty(soup)
        # video = soup.find('div', {'class': 'video-page__row'})
        # if video:
            # psp(video.prettify())
        script = soup.find('script', text=lambda x: 'sources.push' in str(x))
        if script:
            # pretty(script)
            data = str(script.string).replace(' ', '')
            file=quotes(data, "src:'","'")
            # sources = files.split(',')
            # for item in sources:
            #     file = item.rpartition(']')[2]
            #     label = quotes(item, '[', ']')
            #     # psp(file, label)
            #     if file:
            self.add_video("Default", URL(file, base_url=url))
        self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class','panel-content-wide'})
        if container:
            # pretty(container)


            # models=container.find('div',{'class':'starring'})
            # if models:
            # for xref in _iter(container.find_all('a',href=lambda x: '/aktrisa/' in str(x))):
            #     # psp(xref)
            #     href=xref.attrs.get('href','')
            #     self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='blue'))
            cat_container=container.find('dd',{'class':'cat'})
            if cat_container:
                categories=cat_container.find_all('a')
                for category in _iter(categories):
                    # pretty(category)
                    href=category.attrs.get('href','')
                    title=category.attrs.get('title','')
                    self.add_tag(title, URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass

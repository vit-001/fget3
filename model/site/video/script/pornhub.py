# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornhubSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornhub.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/pornhub.png',
                              # menu_items=menu_items,
                              url=URL("https://rt.pornhub.com/video?o=cm", test_string='порно'))

    def get_shrink_name(self):
        return 'PH'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):

        counter=0

        for thumbnail in _iter(soup.find_all('li', {'class': 'videoBox'})):
            if counter<4:
                counter = counter+1
                continue
            try:
                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                # pretty(xref)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-src',thumbnail.img.attrs.get('data-thumb_url',''))
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                label = thumbnail.img.attrs.get('alt')

                duration = thumbnail.find('var', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('span', {'class': 'hd-thumbnail'})
                hd = '' if hd_tag is None else "HD"

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])
            except AttributeError as e:
                print(e.__repr__())

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
        return soup.find('div',{'class':'pagination3'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'player'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'flashvars' in str(x))
            # psp(script)

            flashvars = quotes(str(script).replace(' ', ''), 'qualityItems', ']')
            if flashvars:
                # psp(flashvars)

                sections=flashvars.split('},{')
                for item in sections:
                    # psp(item)
                    text=quotes(item,'"text":"','"')
                    url=quotes(item,'"url":"','"').replace('\\','')
                    # psp(text, url)

                    if url:
                        self.add_video(text, URL(url))

                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'video-detailed-info'})
        if container:
            # pretty(container)

            user=container.find('span', {'class':'usernameBadgesWrapper'})
            if user:
                # pretty(user)


                for item in _iter(user.find_all('a', href=True)):
                    # pretty(item)
                    href=item.attrs.get('href','')+'/videos*'
                    text=collect_string(item)

                    self.add_tag(text, URL(href, base_url=url), style=dict(color='blue'))

            stars=container.find('div', {'class':'pornstarsWrapper'})
            if stars:
                # pretty(stars)


                for item in _iter(stars.find_all('a', href=True)):
                    # pretty(item)
                    href=item.attrs.get('href','')+'/videos*'
                    text=collect_string(item)

                    self.add_tag(text, URL(href, base_url=url), style=dict(color='red'))


            categories=container.find('div', {'class':'categoriesWrapper'})
            if categories:
                # pretty(categories)


                for item in _iter(categories.find_all('a',{'class':'item'})):
                    # pretty(item)
                    href=item.attrs.get('href','')
                    text=collect_string(item)

                    self.add_tag(text, URL(href, base_url=url))

            tags=container.find('div', {'class':'tagsWrapper'})
            if tags:
                # pretty(tags)


                for item in _iter(tags.find_all('a',{'class':'item'})):
                    # pretty(item)
                    href=item.attrs.get('href','')
                    text=collect_string(item)

                    self.add_tag(text, URL(href, base_url=url))


        models=soup.find('div',{'class':'meta-item'})
        if models:
            # pretty(models)
            for xref in _iter(models.find_all('a',href=lambda x: not 'javascript' in str(x))):
                # psp(xref)
                href=xref.attrs.get('href','')
                self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='blue'))

        categories=soup.find('div',{'class':'full-category'})
        if categories:
            # pretty(categories)
            for xref in _iter(categories.find_all('a',href=lambda x: not 'javascript' in str(x))):
                # psp(xref)
                href=xref.attrs.get('href','')
                self.add_tag(collect_string(xref), URL(href, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass

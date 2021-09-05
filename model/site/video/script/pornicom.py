# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornicomSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornicom.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/pornicom.svg',
                              # menu_items=menu_items,
                              url=URL("https://www.pornicom.com/latest-updates/", test_string='adult'))

    def get_shrink_name(self):
        return 'PC'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'thumbs-holder'})
        # pretty(contents)
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'video-thumb'})):

                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                # img=thumbnail.find('img',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-original',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                label = thumbnail.img.attrs.get('alt')

                duration = thumbnail.find('span', {'class': 'time'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('i', {'class': 'icon-hd'})
                hd = '' if hd_tag is None else "HD"

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
        return soup.find('div',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'flashvars' in str(x))
            # psp(script)

            flashvars = quotes(str(script).replace(' ', ''), 'flashvars={', '}')
            if flashvars:
                # psp(flashvars)

                video_url = quotes(flashvars, "video_url:'", "'")
                video_url_text = quotes(flashvars, "video_url_text:'", "'")

                video_alt_url = quotes(flashvars, "video_alt_url:'", "'")
                video_alt_url_text = quotes(flashvars, "video_alt_url_text:'", "'")

                if video_url: self.add_video(video_url_text, URL(video_url, base_url=url))
                if video_alt_url: self.add_video(video_alt_url_text, URL(video_alt_url, base_url=url))

            # for source in _iter(video.find_all('source')):
            #     # psp(source)
            #     if 'http' in source.attrs.get('src',''):
            #         self.add_video(source.attrs.get('title','default'), URL(source.attrs['src']))
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        models=soup.find('div',{'class':'models-holder'})
        if models:
            # pretty(models)
            for xref in _iter(models.find_all('a',href=True)):
                # psp(xref)
                href=xref.attrs.get('href','')
                self.add_tag(collect_string(xref), URL(href, base_url=url), style=dict(color='red'))


        container = soup.find('div', {'class': 'info-holder'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))

        container = soup.find('div', {'class': 'video-tags'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))




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

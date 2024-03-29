# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class CrockotubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('crockotube.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/crockotube.png',
                              # menu_items=menu_items,
                              url=URL("https://www.crockotube.com/allvideos/most_recent/", test_string='tube'))

    def get_shrink_name(self):
        return 'CT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # contents=soup.find('div', {'class':'less-gutter'})
        # pretty(contents)
        # if contents:
        #     # pretty(contents)
            for thumbnail in _iter(soup.find_all('div', {'class': 'video-thumb-wrap'})):

                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True, title=True)
                # img=thumbnail.find('img',href=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=thumbnail.img.attrs.get('data-src',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                label = xref.attrs.get('title')

                duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('span', {'class': 'quality'})
                hd = '' if hd_tag is None else collect_string(hd_tag)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])



    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('ul',{'class':'category'})):
            for item in _iter(container.find_all('a',href=lambda x:'/category/' in str(x))):
                # pretty(item)
                self.add_tag(collect_string_to_array(item)[0], URL(item.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'video-cassete'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'flashvars' in str(x))
            # psp(script)

            flashvars = quotes(str(script).replace(' ', ''), 'flashvars={', '}')
            if flashvars:
                # psp(flashvars)

                video_url = quotes(flashvars, 'video_url:"', '"')
                video_url_text = quotes(flashvars, "video_url_text:'", "'")
                if not video_url_text: video_url_text='default'

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

        container = soup.find('div', {'class': 'block-more'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))

        container = soup.find('div', {'class': 'tags-list'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))


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

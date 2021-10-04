# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class XdpornerSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('xdporner.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        menu_items=dict(Top_Rated_Video=URL('https://xdporner.com/videos.php?sb=l&t=al&p=1*'),
                    Latest_Video=URL('https://xdporner.com/videos.php?sb=d*'))

        view.add_start_button(picture_filename='model/site/resource/xdporner.png',
                              menu_items=menu_items,
                              url=URL("https://xdporner.com/videos.php?sb=d*", test_string='porn'))

    def get_shrink_name(self):
        return 'XD'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # contents=soup.find('div', {'class','thumblist'})
        # if contents:
        #     # psp(contents.prettify())
            for thumbnail in _iter(soup.find_all('div', {'class': 'main-video'})):
                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                href = URL(xref.attrs['href'].strip('.'), base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('span', {'class': 'p-a'})
                dur_time = '' if duration is None else collect_string(duration)


                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'categories-list'})
        if container:
            # psp(container.prettify())
            for tag in container.find_all('a'):
                self.add_tag(tag.attrs['title'], URL(tag.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'id':'pagination'})
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    self.add_page(page.string, URL(page.attrs['href'].strip('./'), base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'].strip('./'), base_url=url), page.attrs['href'])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'id': 'player'})
        if video:
            # pretty(video)
            for source in _iter(video.find_all('source')):
                self.add_video(source.attrs['title'], URL(source.attrs['src'],base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info=soup.find('div',{'class':'description-view_qt5'})
        if info:
            # pretty(info)
            for xref in _iter(info.find_all('a',{'class':"author-view_qt5", 'href':True})):
                # psp(xref)
                href=xref.attrs['href']
                self.add_tag(collect_string(xref),URL(href.strip('.'),base_url=url), style={'color':'red'})
            for xref in _iter(info.find_all('a',{'class':None, 'href':True})):
                # psp(xref)
                href=xref.attrs['href']
                if '/model.php' in href:
                    self.add_tag(collect_string(xref),URL(href.strip('.'),base_url=url), style={'color':'blue'})
            for xref in _iter(info.find_all('a',{'class':"main-keyword", 'href':True})):
                # psp(xref)
                href=xref.attrs['href']
                self.add_tag(collect_string(xref),URL(href.strip('.'),base_url=url))


            # for xref in _iter(info.find_all('a',href=lambda x: not 'javascript' in str(x))):
            #     psp(xref)
            #     href=xref.attrs['href']
            #     if '/user/' in href:
            #         self.add_tag(quotes(href,'/user/','/'),URL(href.replace('/user/','/submitted/'),base_url=url), style={'color':'blue'})
            #     else:
            #         self.add_tag(collect_string(xref), URL(href, base_url=url))


if __name__ == "__main__":
    pass

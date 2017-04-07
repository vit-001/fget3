# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornhdSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornhd.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Featured_Videos=URL('http://www.pornhd.com/?order=featured*'),
                    Newest_Video=URL('http://www.pornhd.com/?order=newest*'),
                    Most_Viewed=URL('http://www.pornhd.com/?order=mostpopular*'),
                    Longest_Video=URL('http://www.pornhd.com/?order=longest*'),
                    Top_Rated_Video=URL('http://www.pornhd.com/?order=toprated*'),
                    Category=URL('http://www.pornhd.com/category?order=alphabetical*'),
                    Channels_Alphabetical=URL('http://www.pornhd.com/channel?order=alphabetical*'),
                    Channels_Most_Popular=URL('http://www.pornhd.com/channel?order=most-popular*'),
                    Channels_Most_Videos=URL('http://www.pornhd.com/channel?order=most-videos*'),
                    Channels_Newest=URL('http://www.pornhd.com/channel?order=newest*'),
                    Pornstars_Alphabetical=URL('https://www.pornhd.com/pornstars?order=alphabetic*'),
                    Pornstars_Most_Popular=URL('https://www.pornhd.com/pornstars?order=most-popular*'),
                    Pornstars_Most_Videos=URL('https://www.pornhd.com/pornstars?order=video-count*')
                    )

        view.add_start_button(picture_filename='model/site/resource/pornhd.svg',
                              menu_items=menu_items,
                              url=URL("http://www.pornhd.com/?order=newest*", test_string='PornHD'))

    def get_shrink_name(self):
        return 'PHD'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbs in _iter(soup.find_all('ul',{'class':'thumbs'})):
            for thumbnail in _iter(thumbs.find_all('li')):
                xref=thumbnail.find('a',{'class':'thumb'})
                if xref:
                    # psp(thumbnail.prettify())
                    href = URL(xref.attrs['href'], base_url=url)

                    img=thumbnail.img
                    thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                    thumb_url = URL(thumb_file, base_url=url)

                    label=img.attrs.get('alt','')

                    duration = thumbnail.find('time')
                    dur_time = '' if duration is None else str(duration.string).strip()

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           {'text':label, 'align':'bottom center'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'tag-150-container'})
        if container:
            for thumbnail in _iter(container.find_all('li')):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a', href=True)
                if xref:
                    # psp(thumbnail.prettify())
                    href = URL(xref.attrs['href'], base_url=url)

                    img=thumbnail.img
                    thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                    thumb_url = URL(thumb_file, base_url=url)

                    label=collect_string(thumbnail)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':label, 'align':'bottom center'}])
            return

        pornstars=soup.find('ul',{'class':'pornstar-tag-list'})
        if pornstars:
            for thumbnail in _iter(pornstars.find_all('li')):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a', href=True)
                if xref:
                    # psp(thumbnail.prettify())
                    href = URL(xref.attrs['href'], base_url=url)

                    img=thumbnail.img
                    thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                    thumb_url = URL(thumb_file, base_url=url)

                    label = img.attrs.get('alt', '')

                    duration = thumbnail.find('div',{'class':'video-count'})
                    dur_time = '' if duration is None else str(duration.string).strip()

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           {'text':label, 'align':'bottom center'}])

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        pager= soup.find('div', {'class':'pager'})
        if pager:
            for page in _iter(pager.find_all('li',{'class':'page'})):
                page_span=page.find('span',{'data-query-key':True, 'data-query-value':True})
                if page_span:
                    label=str(page_span.string).strip()
                    page_url=URL(url.get())
                    page_url.add_query([(page_span.attrs['data-query-key'],page_span.attrs['data-query-value'])])
                    self.add_page(label, page_url)

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'player-container'})
        if container:
            script = str(container.find('script', text=lambda x: 'players.push(' in str(x)).string)
            if script:
                sources=quotes(script.replace(' ',''), "'sources':{", '}' ).split(',')
                for source in sources:
                    split=source.partition(':')
                    label=split[0].strip("'")
                    file=split[2].strip("' ")
                    if file:
                        self.add_video(label, URL(file, base_url=url))
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        def color(xref:str)->str:
            color = None
            if '/channel/' in xref:
                color = 'blue'
            if '/pornstars/' in xref:
                color = 'red'
            return color

        container=soup.find('div',{'class':'section-title'})
        if container:
            for href in _iter(container.find_all('a', href=True)):
                xref=href.attrs['href']
                self.add_tag(str(href.string), URL(xref, base_url=url),style=dict(color=color(xref)))
        tags_container=soup.find('ul',{'class':'video-tag-list'})
        if tags_container:
            for href in _iter(tags_container.find_all('a', href=True)):
                xref=href.attrs['href']
                self.add_tag(collect_string(href), URL(xref, base_url=url),style=dict(color=color(xref)))


if __name__ == "__main__":
    pass

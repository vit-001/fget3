# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class ThumbzillaSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('thumbzilla.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Hottest=URL('https://www.thumbzilla.com/'),
                    Newest=URL('https://www.thumbzilla.com/newest*'),
                    Pornstar_Alphabetical=URL('https://www.thumbzilla.com/pornstars?o=a*'),
                    Pornstar_Videos=URL('https://www.thumbzilla.com/pornstars?o=nv*'),
                    Pornstar_Rank=URL('https://www.thumbzilla.com/pornstars?o=mp*'),
                    Top=URL('https://www.thumbzilla.com/top*'),
                    Trending=URL('https://www.thumbzilla.com/trending*'),
                    Popular=URL('https://www.thumbzilla.com/popular*'),
                    HD=URL('https://www.thumbzilla.com/hd*'),
                    Homemade=URL('https://www.thumbzilla.com/homemade*'))

        view.add_start_button(picture_filename='model/site/resource/thumbzilla.png',
                              menu_items=menu_items,
                              url=URL("https://www.thumbzilla.com/newest*"))

    def get_shrink_name(self):
        return 'TZ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        content=soup.find('section', id='content')
        if content:
            for thumbnail in _iter(content.find_all('a',{'class':'js-thumb'})):
                    href = URL(thumbnail.attrs['href'], base_url=url)

                    img=thumbnail.img
                    thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                    thumb_url = URL(thumb_file, base_url=url)

                    title = thumbnail.find('span',{'class':'title'})
                    label = '' if title is None else str(title.string).strip()

                    duration = thumbnail.find('span',{'class':'duration'})
                    dur_time = '' if duration is None else str(duration.string).strip()

                    hd_span = thumbnail.find('span', {'class': 'hd'})
                    hd = str(hd_span.string).strip() if hd_span else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           {'text': hd, 'align': 'top left'},
                                           {'text':label, 'align':'bottom center'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        content=soup.find('section', id='content')
        if content:
            for star in _iter(content.find_all('li',{'class':'pornstars'})):
                href = URL(star.a.attrs['href'], base_url=url)

                img=star.img
                thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                thumb_url = URL(thumb_file, base_url=url)

                title = star.find('span',{'class':'title'})
                label = '' if title is None else str(title.string).strip()

                duration = star.find('span',text=lambda x: 'Videos' in str(x))
                dur_time = '' if duration is None else str(duration.string).strip()

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': hd, 'align': 'top left'},
                                       {'text':label, 'align':'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('ul', {'class':'categoryList'})
        if container:
            for xref in container.find_all('a',href=True):
                label=str(xref.find('span',{'class':'wrapper'}).contents[0]).strip()
                count=xref.find('span', {'class':'count'})
                num= '(' + count.string + ')' if count.string else ''
                self.add_tag(label+ num,URL(xref.attrs['href'],base_url=url))


    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('section',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        scripts = soup.find_all('script', text=lambda x: 'var pageVar =' in str(x))
        for script in _iter(scripts):
            videovars=quotes(str(script.string).replace(' ',''),"'videoVars':{","}").split(",")
            default=-1
            for var in videovars:
                (label,sep,href)=var.replace('"','').replace('\\','').partition(':')
                if label.startswith('quality_'):
                    if '720' in label:
                        default=len(self.video_data)
                    self.add_video(label, URL(href))
            self.set_default_video(default)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'videoInfoTop'})
        if container:
            # psp(container.prettify())
            stars=container.find('span',{'class':'stars'})
            if stars:
                for star in _iter(stars.find_all('a',href=True)):
                    self.add_tag(star.string,URL(star.attrs['href'],base_url=url),style=dict(color='red'))
            categories = container.find('span', {'class': 'categories'})
            if categories:
                for category in _iter(categories.find_all('a', href=True)):
                    self.add_tag(category.string, URL(category.attrs['href'], base_url=url))
            tags = container.find('span', {'class': 'tags'})
            if tags:
                for tag in _iter(tags.find_all('a', href=True)):
                    self.add_tag(tag.string, URL(tag.attrs['href'], base_url=url))

if __name__ == "__main__":
    pass

# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, pretty, collect_string, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornComSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('.porn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Channels=URL('http://www.porn.com/channels*'),
                    Stars=URL('http://www.porn.com/pornstars?o=n*'),
                    Categories=URL('http://www.porn.com/categories*'),
                    Video_Longest=URL('http://www.porn.com/videos?o=l*'),
                    Video_Newest=URL('http://www.porn.com/videos'),
                    Video_Top_Rated_Week=URL('http://www.porn.com/videos?o=r7*'),
                    Video_Top_Rated_Month=URL('http://www.porn.com/videos?o=r30*'),
                    Video_Top_Rated_All_Time=URL('http://www.porn.com/videos?o=r*'),
                    Video_Popular_Week=URL('http://www.porn.com/videos?o=f7*'),
                    Video_Popular_Month=URL('http://www.porn.com/videos?o=f30*'),
                    Video_Popular_All_Time=URL('http://www.porn.com/videos?o=f*'),
                    Video_Viewed_Week=URL('http://www.porn.com/videos?o=v7*'),
                    Video_Viewed_Month=URL('http://www.porn.com/videos?o=v30*'),
                    Video_Viewed_All_Time=URL('http://www.porn.com/videos?o=v*')
                    )

        view.add_start_button(picture_filename='model/site/resource/porncom.svg',
                              menu_items=menu_items,
                              url=URL("http://www.porn.com/videos*", test_string='PORN.COM', load_method='SELENIUM'))

    def get_shrink_name(self):
        return 'PC'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        psp(soup)
        container=soup.find('section',{'class':['videos','categories','profiles','models','channels']})
        if container:
            for item in _iter(container.find_all('div',{'class':'item'})):
                try:
                    href = URL(item.a.attrs['href'], base_url=url)
                    thumb_url = URL(item.img.attrs['src'], base_url=url)
                    label = item.img.attrs.get('alt', '')

                    meta=item.find('div',{'class':'meta'})
                    dur_time=''
                    if meta:
                        if meta.find('span'):
                            dur_time = collect_string(meta.span)

                    hd_span = item.find('span', {'class': ['hd']})
                    hd = '  HD' if hd_span else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
                except KeyError:
                    pass

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        # adding alpha to thumbs
        alpha_container = soup.find('div', {'class': 'alpha'})
        if alpha_container is not None:
            for alpha in _iter(alpha_container.find_all('a')):
                self.add_tag(str(alpha.string), URL(alpha.attrs['href'], base_url=url))

        # adding tags to thumbs
        tags_container = soup.find('aside')
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a', id=None)):
                if '#' in tag.get('href','#'):
                    continue
                self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('nav', {'class': 'pager'})

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and str(page.string).strip().isdigit():
                    self.add_page(page.string.strip(), URL(page.attrs['href'], base_url=url))
                elif 'next' in page.attrs['class']:
                    self.add_page('>', URL(page.attrs['href'], base_url=url))
                elif 'prev' in page.attrs['class']:
                    self.add_page('<', URL(page.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        head = soup.find('head')
        if head:
            script = head.find('script', text=lambda x: 'streams:' in str(x))
            if script:
                data = str(script).replace(' ', '')
                sources = quotes(data, 'streams:[{', '}]').split('},{')
                for f in sources:
                    label = quotes(f, 'id:"', '"')
                    url = URL(quotes(f, 'url:"', '"'), base_url=url)
                    if url.contain('.mp4'):
                        self.add_video(label, url)
                self.set_default_video(-1)

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return super().parse_video_title(soup, url).rpartition('-')[0]

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        stars=soup.find('div',{'class':'pornstars'})
        if stars:
            for item in _iter(stars.find_all('a', href=lambda x: '#' not in x)):
                self.add_tag(collect_string(item), URL(item.attrs['href']+'/videos', base_url=url), style=dict(color='magenta'))

        tags = soup.find('div', {'class': 'meta-tags'})
        for item in _iter(tags.find_all('a', href=lambda x: '#' not in x)):
            color = None
            href = item.attrs['href']
            if '/pornstars/' in href:
                color = 'magenta'
                href += '/videos'
            if '/profile/' in href:
                color = 'blue'
                href += '/videos'
            if '/channels/' in href:
                color = 'blue'
            if '/playlists/' in href:
                color = 'brown'
            label = collect_string(item)
            self.add_tag(label, URL(href, base_url=url), style=dict(color=color))


if __name__ == "__main__":
    pass

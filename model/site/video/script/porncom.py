# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes

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

        view.add_start_button(name='PornCom',
                              picture_filename='model/site/resource/porncom.svg',
                              menu_items=menu_items,
                              url=URL("http://www.porn.com/videos*", test_string='PORN.COM'))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        mainw = soup.find('div', {'class': ['mainw', 'profileContent']})
        thumbs_list = mainw.find('ul', {'class': ['listThumbs', 'listChannels', 'listProfiles', 'listTags']})
        if thumbs_list is not None:
            for thumbnail in _iter(thumbs_list.find_all('li')):
                href = thumbnail.a.attrs['href']
                url = URL(href, base_url=url)

                hd_span = thumbnail.find('span', {'class': 'hd'})
                hd = '' if hd_span is None else '  HD'

                if '/videos/' in href or '/pornstars/' in href:
                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                    duration = thumbnail.find('span', {'class': 'added'})
                    dur_time = '' if duration is None else str(duration.string)

                    caption = thumbnail.find('a', {'class': ['title', 'name']})
                    label = '' if caption is None else str(caption.string)

                    self.add_thumb(thumb_url=thumb_url, href=url, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left', 'bold': True}])
                elif '/channels/' in href:
                    logo = thumbnail.find('img', {'class': 'logo'})
                    thumb_url = URL(logo.attrs['src'], base_url=url)

                    title = thumbnail.find('span', {'class': 'title'})
                    label = '' if title is None else str(title.string)

                    count_span = thumbnail.find('span', {'class': 'count'})
                    count = '' if count_span is None else str(count_span.string)

                    self.add_thumb(thumb_url=thumb_url, href=url, popup=label,
                                   labels=[{'text': count, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'PC '+ url.get().partition('porn.com/')[2]

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        # adding tags to thumbs
        tags_container = soup.find('div', {'class': 'listFilters'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a', {'class': None})):
                title = tag.attrs.get('title', '')
                count = tag.find('span', {'class': 'count'})
                count_str = '' if count is None else count.string
                self.add_tag('{0}({1})'.format(title, count_str), URL(tag.attrs['href'], base_url=url))

        # adding alpha to thumbs
        alpha_container = soup.find('div', {'class': 'alpha'})
        if alpha_container is not None:
            for alpha in _iter(alpha_container.find_all('a')):
                self.add_tag(str(alpha.string), URL(alpha.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pager'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        head = soup.find('head')
        if head is not None:

            script = head.find('script', text=lambda x: 'streams:' in str(x))
            if script is not None:
                data = str(script).replace(' ', '')
                sources = quotes(data, 'streams:[{', '}]').split('},{')
                for f in sources:
                    label = quotes(f, 'id:"', '"')
                    url = URL(quotes(f, 'url:"', '"'), base_url=url)
                    if url.contain('.mp4'):
                        self.add_video(label, url)
                self.set_default_video(-1)

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().rpartition('/')[2].rpartition('-')[0]

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        vid_source = soup.find('div', {'class': 'vidSource'})
        for item in _iter(vid_source.find_all('a', href=lambda x: '#' not in x)):
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
            label = str(item.string)
            self.add_tag(label, URL(href, base_url=url), style=dict(color=color))


if __name__ == "__main__":
    pass

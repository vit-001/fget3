__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornmzSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornmz.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(New=URL('https://pornmz.com/?filter=latest*'),
                    Best=URL('https://pornmz.com/?filter=popular*'),
                    MostViewed=URL('https://pornmz.com/?filter=most-viewed*'),
                    Longest=URL('https://pornmz.com/?filter=longest*')
                    )

        view.add_start_button(picture_filename='model/site/resource/PornMZ.png',
                              menu_items=menu_items,
                              url=URL("https://pornmz.com/"))

    def get_shrink_name(self):
        return 'PW'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'videos-list'})
        if contents:
            # pretty(contents)

            for thumbnail in _iter(contents.find_all('article', {'class':'thumb-block'})):
                try:
                    # pretty(thumbnail)

                    href = URL(thumbnail.a.attrs['href'], base_url=url)
                    # style= thumbnail.find('div',{'class':'img-src', 'style':True})
                    video=thumbnail.find('video')
                    thumb_url = URL(video.attrs.get('poster'))

                    title_tag = thumbnail.find('span', {'class': 'title'})
                    label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('span', {'class': 'duration'})
                    dur_time = '' if duration is None else str(duration.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           ])
                except AttributeError:
                    pass

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu=soup.find('ul',{'class':'dropdown-menu'})
        if menu:
            for tag in menu.find_all('a', href=True):
                self.add_tag(str(tag.string).strip(),
                             URL(tag.attrs['href'], base_url=url),
                             style=dict(color='blue'))

        tags=soup.find('section', id='footer-tag')
        if tags:
            for tag in tags.find_all('a', href=True):
                self.add_tag(str(tag.string).strip(),
                             URL(tag.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'class':'pagination'})
        # psp(url.get())
        if container:
            # baseurl=url.get().rstrip('/').rstrip('1234567890')+'/'
            # baseurl = url.get().rstrip('/')
            # if baseurl.rpartition('/')[2].isdecimal():
            #     baseurl=baseurl.rpartition('/')[0]

            for page in _iter(container.find_all('a', {'href': True})):
                # if page.string and str(page.string).strip().isdigit():
                    href=page.attrs['href']
                    # if href == "#videos":
                    #     param=page.attrs['data-parameters']
                    #     pagenum=param.rpartition('from:')[2]
                    #     href=baseurl+'/'+pagenum+'/'

                    self.add_page(page.string.strip(), URL(href, base_url=url))
    #
    # def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
    #     pretty(soup.find('div',{'class':'pagination-holder'}))
    #     return soup.find('div',{'class':'pagination-holder'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'responsive-player'})
        if container:
            # pretty(container)
            frame=container.find('iframe')
            if frame:
                # psp(frame)
                file_url=URL(frame.attrs['src'],base_url=url)
                # psp(file_url.get())
                filedata=FLData(file_url,'')

                self._result_type = 'video'
                self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        soup=BeautifulSoup(fldata.text, 'html.parser')
        # pretty(soup)
        player=soup.find('div', {'class':'wps-player'})
        if player:
        # pretty(player)
            video=player.find('video')
            if video:
                for source in _iter(video.find_all('source', src=True)):
                    # pretty(source)
                    self.add_video(source.attrs.get('label','???'), URL(source.attrs.get('src'),base_url=fldata.url))
            # self.set_default_video(-1)
                self.generate_video_view()
        else:
            print('No video here')

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'tags-list'})

        # pretty(container)

        for href in _iter(container.find_all('a',href=lambda x: '/id=pmactor/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})
        #
        # for href in _iter(container.find_all('a',href=lambda x: '/models/' in str(x))):
        #     # psp(href)
        #     self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})
        #
        for href in _iter(container.find_all('a',href=lambda x: '/c/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))
        #
        for href in _iter(container.find_all('a',href=lambda x: '/s/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))

if __name__ == "__main__":
    pass

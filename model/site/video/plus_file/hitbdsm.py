__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class HitbdsmSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('hitbdsm.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        # menu_items=dict(Pornstars=URL('http://toseeporn.com/Actor*'),
        #             Home=URL('http://toseeporn.com/*'),
        #             Search_Example=URL('http://toseeporn.com/Search=asian%20sex%20diary*')
        #             )

        view.add_start_button(picture_filename='model/site/resource/hitbdsm.png',
                              # menu_items=menu_items,
                              url=URL("https://hitbdsm.com/?filter=latest*"))

    def get_shrink_name(self):
        return 'HB'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('article', {'class':'thumb-block'})):
            try:
                # pretty(thumbnail)
                xref=thumbnail.find('a', href=True, title=True)
                img=thumbnail.find('img', {'data-src':True})

                if xref and img:

                    href = URL(xref.attrs.get('href'), base_url=url)
                    thumb_url = URL(img.attrs.get('data-src'), base_url=url)

                    label = xref.attrs.get('title')

                    duration = thumbnail.find('span', {'class': 'duration'})
                    dur_time = '' if duration is None else collect_string(duration)

                    hd_span = str(thumbnail.find('span', {'class': 'video-resolution'}))
                    hd = 'HD' if 'HD.png' in hd_span else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           {'text': hd, 'align': 'top left'}])
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

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video=soup.find('div', {'class':'responsive-player'})
        if video:
            # pretty(video)
            frame = video.find('iframe', src=True)
            if frame:
                # pretty(frame)

                filedata=FLData(URL(frame.attrs.get('src')),'')
            #
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
        stars=soup.find('div',{'id':'video-actors'})
        if stars:
            for star in stars.find_all('a',href=True, title=True):
                self.add_tag(star.attrs.get('title'), URL(star.attrs.get('href'),base_url=url), style=dict(color='red'))

        tags=soup.find('div',{'class':'tags'})
        if tags:
            for tag in tags.find_all('a',href=True, title=True):
                self.add_tag(tag.attrs.get('title'), URL(tag.attrs.get('href'),base_url=url))

if __name__ == "__main__":
    pass

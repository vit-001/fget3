__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class ToseepornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('toseeporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Pornstars=URL('http://toseeporn.com/Actor*'),
                    Home=URL('http://toseeporn.com/*'),
                    Search_Example=URL('http://toseeporn.com/Search=asian%20sex%20diary*')
                    )

        view.add_start_button(picture_filename='model/site/resource/tooseeporn.png',
                              menu_items=menu_items,
                              url=URL("http://toseeporn.com/Category/West%20Porn*"))

    def get_shrink_name(self):
        return 'TSP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('section', {'class':'content-video'})):
            try:
                # psp(thumbnail.prettify())

                href = URL(thumbnail.a.attrs['href'], base_url=url)
                style= thumbnail.find('div',{'class':'img-src', 'style':True})
                thumb_url = URL(quotes(str(style['style']),"'","'"))

                label = str(thumbnail.h3.string).strip()

                duration = thumbnail.find('span', {'class': 'video-time'})
                dur_time = '' if duration is None else str(duration.string)

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
        return soup.find('div',{'class':'content-pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        script=soup.find('script', text=lambda x: 'angular.' in str(x))
        if script:
            json_file_url=URL(quotes(script.string.replace(' ',''),"host:'","'"),base_url=url)
            filedata=FLData(json_file_url,'')

            self._result_type = 'video'
            self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        data=json.loads(fldata.text)
        for item in data['mediaSources']:
            self.add_video(item['quality'],URL(item['source']))
        self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        stars=soup.find('div',{'class':'porn-star'})
        if stars:
            for star in stars.find_all('figure'):

                self.add_tag(str(star.figcaption.string).strip(),
                             URL(star.a.attrs['href'],base_url=url),
                             style=dict(color='red'))

        tags=soup.find('div',{'class':'tag-area'})
        if tags:
            for tag in tags.find_all('a', href=True):
                self.add_tag(str(tag.string).strip(),
                             URL(tag.attrs['href'], base_url=url))

if __name__ == "__main__":
    pass

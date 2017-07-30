__author__ = 'Vit'
from bs4 import BeautifulSoup
from urllib.parse import unquote

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser

class YPData(FLData):
    def __init__(self, url: URL, part: str):
        super().__init__(url, '')
        self.part=part

class SexixSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('sexix.net/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):

        view.add_start_button(picture_filename='model/site/resource/sexis.png',
                              url=URL("http://sexix.net/?orderby=date*"))

    def get_shrink_name(self):
        return 'SXX'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'thumb'})):

            href = URL(thumbnail.a.attrs['href'], base_url=url)
            description = thumbnail.a.img.attrs['alt']
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                           labels=[{'text': description, 'align': 'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'wp-pagenavi'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        cloud=soup.find('div', {'class':'tagcloud'})
        tags=dict()
        for href in _iter(cloud.find_all('a')):
            tag_href=href.attrs['href']
            label=href.string
            if '/videotag/' in tag_href:
                tags[label]=URL(tag_href)

        for label in sorted(tags):
            self.add_tag(label,tags[label])

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video_container=soup.find('div',{'class':'videoContainer'})
        if video_container:
            # psp(video_container)
            source_file=URL(video_container.iframe.attrs['src'], base_url=url,referer=url)
            filedata=FLData(source_file,'')

            self._result_type = 'video'
            self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        playlist_file=URL(quotes(fldata.text, "jwplayer().load('", "'")+'*')
        filedata = FLData(playlist_file, '')
        self.model.loader.start_load_file(filedata, self.continue_parse_video2)

    def continue_parse_video2(self, fldata:FLData):
        playlist=BeautifulSoup(fldata.text.replace('jwplayer:source','jjj'), "html.parser")
        for item in playlist.find_all('jjj'):
            # psp(unquote(str(item)))
            if item.attrs.get('file',''):
                video_url=URL(unquote(str(item.attrs['file'])))
                label=item.attrs['label']
                self.add_video(label,video_url)
        self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info=soup.find('div',{'id':'info'})
        for href in _iter(info.find_all('a')):
            tag_href=href.attrs['href']
            label=href.string
            if '/videotag/' in tag_href:
                self.add_tag(label,URL(tag_href))

if __name__ == "__main__":
    pass

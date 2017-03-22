# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornbrazeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornbraze.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_Most_Recsent=URL('http://pornbraze.com/recent/'),
                        Videos_HD=URL('http://pornbraze.com/hd-porn/'),
                        Videos_Longest=URL('http://pornbraze.com/longest/'),
                        Videos_Downloaded=URL('http://pornbraze.com/downloaded/'),
                        Videos_Most_Popular=URL('http://pornbraze.com/popular/'),  #
                        DVDs=URL('http://pornbraze.com/dvd/'),
                        Channels=URL('http://pornbraze.com/channels/')
                        )

        view.add_start_button(picture_filename='model/site/resource/pornbaze.png',
                              menu_items=menu_items,
                              url=URL("http://pornbraze.com/recent/"))

    def get_shrink_name(self):
        return 'PBZ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'video'})):

            href = URL(thumbnail.a.attrs['href'], base_url=url)
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
            label=thumbnail.img.attrs.get('alt','')

            duration = thumbnail.find('span', {'class': 'video-overlay'})
            dur_time = '' if duration is None else str(duration.string)

            hd_span = thumbnail.find('span', {'class': 'hdmovie-icon'})
            hd = 'HD' if hd_span else ''

            self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                           labels=[{'text':dur_time, 'align':'top right'},
                                   {'text':label, 'align':'bottom center'},
                                   {'text': hd, 'align': 'top left'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('li', {'class': 'channel'})):
            href = URL(str(thumbnail.a.attrs['href']).rstrip('/')+'/', base_url=url)

            avatar=thumbnail.find('div',{'class':'avatar'})
            thumb_url = URL(avatar.img.attrs['src'], base_url=url)
            label=avatar.img.attrs.get('alt','')

            duration = thumbnail.find('span', {'class': 'infolitte'})
            dur_time = '' if duration is None else str(duration.string)+ ' videos'

            self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                           labels=[{'text':dur_time, 'align':'top right'},
                                   {'text':label, 'align':'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'pagination'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        panel=soup.find('div',{'class':'panel'})
        if panel:
            for categorie in _iter(panel.find_all('a')):
                label=str(categorie.contents[0]).strip()
                href=URL(categorie.attrs['href'],base_url=url)
                self.add_tag(label,href)

    def parse_video(self, soup: BeautifulSoup, url: URL):
        player_container = soup.find('div', {'id':'player'})
        if player_container:
            script=player_container.find('script', text=lambda text: 'jwplayer' in str(text))
            if script:
                text=script.string
                if 'sources:[' in text:
                    sources = quotes(text, 'sources:[', ']')
                    j = json.loads('['+sources+']')
                    for j_data in j:
                        if j_data['file'] is not '':
                            self.add_video(j_data['label'],URL(j_data['file']+'*'))
                            self.set_default_video(-1)
                elif 'sources:' in text:
                    container = soup.find('div', {'class': 'content-video'})
                    if container:
                        script = container.find('script',{'src':lambda x: '/player/' in str(x)})
                        if script:
                            script_url=URL(script.attrs['src'],base_url=url)
                            filedata = FLData(script_url, '')

                            self._result_type = 'video'
                            self.model.loader.start_load_file(filedata, self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        bitrates=quotes(fldata.text,"'bitrates':[{","}]").split('},{')
        for item in bitrates:
            file=quotes(item,"'file':'","'")
            label=quotes(item,'label:"','"')
            self.add_video(label,URL(file))
        self.set_default_video(-1)
        self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # info_box=soup.find('div',{'class':'content-container'})
        for info_box in _iter(soup.find_all('div',{'class':'content-container'})):
            # psp(info_box.prettify())
            for href in _iter(info_box.find_all('a', href=True)):
                psp(href.prettify())
                label=collect_string(href)
                href_url=URL(href.attrs['href'],base_url=url)
                print(label,href_url)

                color=None

                if href_url.contain('/users/'):
                    color='blue'
                    href_url=URL(href_url.get()+'/videos/public/')

                if href_url.contain('/pornstar/'):
                    color='red'

                self.add_tag(label,href_url,style=dict(color=color))

if __name__ == "__main__":
    pass

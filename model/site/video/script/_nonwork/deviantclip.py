# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class DeviantclipSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('deviantclip.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Galleries_Recent=URL('http://www.deviantclip.com/galleries?sort=recent*'),
                        Galleries_Most_Pictures=URL('http://www.deviantclip.com/galleries?sort=pictures*'),
                        Galleries_Top_Rated=URL('http://www.deviantclip.com/galleries?sort=rated*'),
                        Galleries_Most_Viewed=URL('http://www.deviantclip.com/galleries?sort=viewed*'),
                        Videos_Longest=URL('http://www.deviantclip.com/videos?sort=longest*'),
                        Videos_Most_Popular=URL('http://www.deviantclip.com/videos?sort=popular*'),
                        Videos_Recent=URL('http://www.deviantclip.com/videos*'),
                        Videos_Most_Viewed=URL('http://www.deviantclip.com/videos?sort=viewed*'),
                        Videos_Top_Rated=URL('http://www.deviantclip.com/videos?sort=rated*'),
                        Videos_Featured=URL('http://www.deviantclip.com/videos?sort=editorchoice*'))

        view.add_start_button(picture_filename='model/site/resource/deviantclip.png',
                              menu_items=menu_items,
                              url=URL("http://www.deviantclip.com/videos*"))

    def get_shrink_name(self):
        return 'DC'


    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('span', {'class': 'thumb_container_box'})):
            try:
            #     psp(thumbnail.prettify())
                a=thumbnail.find('a',{'class':'video'})
                if a:
                    href = URL(a.attrs['href'], base_url=url)
                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                    label=thumbnail.img.attrs.get('alt','')

                    duration = thumbnail.find('span', {'class': 'lenght_pics'})
                    dur_time = '' if duration is None else str(duration.contents[0]).strip(' -')


                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           {'text':label, 'align':'bottom center'}])

                a = thumbnail.find('a', {'class': 'picture'})
                if a:
                    href = URL(a.attrs['href'], base_url=url)
                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                    label = thumbnail.img.attrs.get('alt', '')

                    lenght_pics = thumbnail.find('span', {'class': 'lenght_pics'})
                    pics = '' if lenght_pics is None else str(lenght_pics.contents[0]).strip(' -')

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': pics, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'}])


            except AttributeError:
                pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'main-sectionpaging'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        categories=soup.find('div',{'id':'categories'})

        for tag in _iter(categories.find_all('a')):
            self.add_tag(collect_string(tag),URL(tag.attrs['href']+'/videos?sort=recent*', base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video')
        if video:
            source=video.find('source')
            if source:
                src=video.source.attrs.get('src',None)
                if src:
                    self.add_video('default',URL(src))
                    return

        player=soup.find('div',{'class', 'player'})
        if player:
            embed=player.find('embed')
            if embed:
                href = URL(embed.attrs['src'])
                self.add_video('default', href)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info_box=soup.find('div',{'class':'bouton'})
        if info_box:
            for tag in _iter(info_box.find_all('a')):
                try:
                    label=tag.string.strip()
                    href=tag.attrs['href']

                    if '/s/' not in href:
                        href+='/videos?sort=recent'
                    self.add_tag(label,URL(href+'*', base_url=url))
                except AttributeError:
                    pass

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        slideshow=soup.find('div',{'id':'slideshow'})
        if slideshow:
            for slide in _iter(slideshow.find_all('a',{'class':'gal'})):
                src=URL(slide.img.attrs['src'])
                filename=src.get_path()+src.get().rpartition('/')[2].partition('?')[0]
                self.add_picture(filename,src)

    def parse_pictures_tags(self, soup: BeautifulSoup, url: URL):
        self.parse_video_tags(soup,url)

if __name__ == "__main__":
    pass

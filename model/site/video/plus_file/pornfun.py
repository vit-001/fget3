# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes , psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornfunSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornfun.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_New=URL('http://pornfun.com/latest-updates/'),
                    Videos_Most_Popular_Today=URL('http://pornfun.com/most-popular/today/'),
                    Videos_Most_Popular_Week=URL('http://pornfun.com/most-popular/week/'),
                    Videos_Most_Popular_Month=URL('http://pornfun.com/most-popular/month/'),
                    Videos_Most_Popular_All_Time=URL('http://pornfun.com/most-popular/'),
                    Videos_Top_Rated_Today=URL('http://pornfun.com/top-rated/today/'),
                    Videos_Top_Rated_Week=URL('http://pornfun.com/top-rated/week/'),
                    Videos_Top_Rated_Month=URL('http://pornfun.comtop-rated/month/'),
                    Videos_Top_Rated_All_Time=URL('http://pornfun.com/top-rated/'),
                    Videos_Longest=URL('http://pornfun.com/longest/'),
                    Video_Categories=URL('http://pornfun.com/categories/'),
                    Photo_Categories=URL('http://pornfun.com/albums/categories/'),
                    Photo_New=URL('http://pornfun.com/albums/'),
                    Photo_Popular=URL('http://pornfun.com/albums/most-popular/'),
                    Photo_Top_Rated=URL('http://pornfun.com/albums/top-rated/')
                    )

        view.add_start_button(picture_filename='model/site/resource/pornfun.png',
                              menu_items=menu_items,
                              url=URL("http://pornfun.com/latest-updates/"))

    def get_shrink_name(self):
        return 'PF'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for content in _iter(soup.find_all('div', {'class':'content'})):
            for thumbnail in _iter(content.find_all('li', {'class': 'thumb'})):
                href = URL(thumbnail.a.attrs['href'], base_url=url)

                name = thumbnail.find('span', {'class': 'thumb-title'})
                description = '' if name is None else str(name.string)
                thumb_url = URL(thumbnail.img.attrs['data-original'], base_url=url)

                duration = thumbnail.find('span', {'class': ['duration', 'counter']})
                dur_time = '' if duration is None else str(duration.string)

                if dur_time != 'Link':
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        categories=soup.find('ul',{'class':'thumbs-categories'})
        if categories:
            for thumbnail in _iter(categories.find_all('li', {'class': 'thumb-category'})):
                # psp(thumbnail.attrs['class'])
                # psp(thumbnail.prettify())

                href = URL(thumbnail.a.attrs['href'], base_url=url)

                name = thumbnail.find('span', {'class': 'category-title'})
                description = '' if name is None else str(name.string)
                thumb_url = URL(thumbnail.img.attrs['data-original'], base_url=url)

                count = thumbnail.find('span', {'class': 'added'})
                counter = '' if count is None else str(count.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': counter, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        list_cat=soup.find('div', {'class', 'list-categories'})
        for href in _iter(list_cat.find_all('a')):
            self.add_tag(str(href.attrs['title']), URL(href.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'class': 'player-holder'})
        if content is not None:
            script = content.find('script', text=lambda x: 'video_url:' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, "video_url:'", "'")

                source_file=URL(file+'*', base_url=url)
                filedata=FLData(source_file,'',find_redirect_location=True)

                self._result_type = 'video'
                self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        if fldata.redirect_location:
            self.add_video('default', fldata.redirect_location)
        else:
            self.add_video('default', fldata.url)
        self.generate_video_view()


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        user_info= soup.find('div', {'class':'user-info'})
        if user_info:
            self.add_tag(str(user_info.a.attrs['title'])+' videos', URL(user_info.a.attrs['href']+'public_videos/', base_url=url),
                         style={'color': 'blue'})

            self.add_tag(str(user_info.a.attrs['title']) + 'albums',
                         URL(user_info.a.attrs['href'] + 'albums/', base_url=url),
                         style={'color': 'blue'})

        specification=soup.find('div', {'class':'specification'})
        if specification:
            for href in _iter(specification.find_all('a')):
                self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        gallery=soup.find('div',{'class':'ad-gallery'})
        if gallery:
            for href in _iter(gallery.find_all('a', {'data-image':True})):
                image_url=URL(href.attrs['data-image'])
                filename=image_url.get_path()+image_url.get().rpartition('/')[2]
                self.add_picture(filename, image_url)

    def parse_pictures_tags(self, soup: BeautifulSoup, url: URL):
        self.parse_video_tags(soup,url)

if __name__ == "__main__":
    pass

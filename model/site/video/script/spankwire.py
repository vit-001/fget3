# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class SpankwireSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('spankwire.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Categories=URL('http://www.spankwire.com/categories/Straight*'),
            HD=URL('http://www.spankwire.com/categories/Straight/HD/Submitted/83*'),
            Longest_All_Time=URL('http://www.spankwire.com/home1/Straight/All_Time/Duration*'),
            Top_Rated_Today=URL('http://www.spankwire.com/home1/Straight/Today/Rating*'),
            Top_Rated_Week=URL('http://www.spankwire.com/home1/Straight/Week/Rating*'),
            Top_Rated_Month=URL('http://www.spankwire.com/home1/Straight/Month/Rating*'),
            Top_Rated_Year=URL('http://www.spankwire.com/home1/Straight/Year/Rating*'),
            Top_Rated_All_time=URL('http://www.spankwire.com/home1/Straight/All_Time/Rating*'),
            Most_Viewed_Today=URL('http://www.spankwire.com/home1/Straight/Today/Views*'),
            Most_Viewed_Week=URL('http://www.spankwire.com/home1/Straight/Week/Views*'),
            Most_Viewed_Month=URL('http://www.spankwire.com/home1/Straight/Month/Views*'),
            Most_Viewed_Year=URL('http://www.spankwire.com/home1/Straight/Year/Views*'),
            Most_Viewed_All_time=URL('http://www.spankwire.com/home1/Straight/All_Time/Views*'))

        view.add_start_button(picture_filename='model/site/resource/spankwire.png',
                              menu_items=menu_items,
                              url=URL("https://www.spankwire.com/home2/Straight/Upcoming/All_Time/Submitted*", test_string='Spankwire'))

    def get_shrink_name(self):
        return 'SKW'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div',{'class':'thumb-info-wrapper'})):
            # psp(thumbnail.prettify())
            try:
                href = URL(thumbnail.a.attrs['href'], base_url=url)

                img=thumbnail.img
                thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                thumb_url = URL(thumb_file, base_url=url)

                label=img.attrs.get('alt','')

                duration = thumbnail.find('div',{'class':'info-box'})
                dur_time = '' if duration is None else str(duration.contents[0]).strip()

                hd_div = thumbnail.find('div', {'class': 'hdIcon'})
                hd = '' if hd_div is None else '  HD'

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text': hd, 'align': 'top left'},
                                       {'text':label, 'align':'bottom center'}])
            except AttributeError:
                pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'pager'})

    def parse_others(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div',{'class':'category-thumb'})):
            # psp(thumbnail.prettify())
            try:
                href = URL(thumbnail.a.attrs['href'], base_url=url)

                img=thumbnail.img
                thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                thumb_url = URL(thumb_file, base_url=url)

                label=img.attrs.get('alt','')

                duration = thumbnail.find('span')
                dur_time = '' if duration is None else str(duration.string)

                hd_div = thumbnail.find('div', {'class': 'hdIcon'})
                hd = '' if hd_div is None else '  HD'

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text': hd, 'align': 'top left'},
                                       {'text':label, 'align':'bottom center'}])
            except AttributeError:
                pass

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', id='videoContainer')
        if video:
            script = video.find('script', text=lambda x: 'playerData.cdnPath' in str(x))
            # psp(script.string)
            if script:
                data = str(script.string).replace(' ', '').partition('playerData.cdnPath')[2]
                while data:
                    parts=data.partition(';')
                    pair=parts[0].partition('=')
                    data=data.partition('playerData.cdnPath')[2]

                    label=pair[0]
                    href=pair[2].strip("' ")

                    if href.startswith('http://') or href.startswith('https://'):
                        self.add_video(label, URL(href))
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        video_info=soup.find('div',{'class':'video-info-uploaded'})
        if video_info:
            user_href=video_info.find('a', href=lambda x: '/user/' in str(x))
            if user_href:
                self.add_tag(user_href.string,
                             URL(user_href.attrs['href'],base_url=url),
                             style=dict(color='blue'))

            for cat in _iter(video_info.find_all('a', id='categoryLink', href=True)):
                self.add_tag(cat.string, URL(cat.attrs['href'],base_url=url))

        tags_container=soup.find('div',{'class':'video-info-row-wrapper'})
        if tags_container:
            for tag in _iter(tags_container.find_all('a', href=True)):
                self.add_tag(tag.string,URL(tag.attrs['href'],base_url=url))

if __name__ == "__main__":
    pass

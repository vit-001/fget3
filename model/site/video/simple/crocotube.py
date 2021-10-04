# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class CrocotubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('crocotube.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/crocotube.png',
                              # menu_items=menu_items,
                              url=URL("https://crocotube.com/", test_string='porn'))

    def get_shrink_name(self):
        return 'TH'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'ct-videos-list'})
        # pretty(contents)
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'thumb'})):

                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                img=thumbnail.find('img',src=True,alt=True)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=img.attrs.get('src','')
                thumb_url = URL(img_url, base_url=url)

                # title_tag = thumbnail.find('div', {'class': 'th-title'})
                # title = thumbnail.find('strong', {'class': 'title'})
                label=img.get('alt','')

                duration = thumbnail.find('div', {'class': 'ct-video-thumb-duration'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('div', {'class': 'ct-video-thumb-hd-icon'})
                hd = '' if hd_tag is None else 'HD'

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}
                               ])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'ct-pagination'})

    # def parse_pagination(self, soup: BeautifulSoup, url: URL):
    #     container = self.get_pagination_container(soup)
    #     if container:
    #         # pretty(container)
    #         for page in _iter(container.find_all('a', {'href': True})):
    #             if page.string and str(page.string).strip().isdigit():
    #                 href=page.attrs['href']
    #                 if '#videos' in href:
    #                     url_txt=url.get().strip('/')
    #                     part=url_txt.rpartition('/')
    #
    #                     if part[2].isdigit():
    #                         url_txt=part[0]
    #
    #
    #                     href=url_txt+'/'+quotes(str(page),'from:','"')+'/'
    #
    #                 self.add_page(page.string, URL(href, base_url=url))
    #                 # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])


    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video', {'id': 'bravoplayer'})
        if video:
            pretty(video)
            for source in _iter(video.find_all('source')):
                self.add_video(source.attrs.get('title','default'), URL(source.attrs['src']))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'ct-video-under-tags'})
        # pretty(container)

        if container:
            for item in _iter(container.find_all('a', href=True)):
                # pretty(item)
                href = item.attrs.get('href', '')
                # self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='red'))

                if '/pornstars/' in href:
                    self.add_tag(collect_string(item),URL(href,base_url=url), style={'color':'red'})
                else:
                    self.add_tag(collect_string(item), URL(href, base_url=url))



        container = soup.find('div', {'class': 'upper-tags'})
        # pretty(container)

        if container:
            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))


    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        head= soup.find('head')
        title=collect_string(head.find('title'))
        # psp(title)
        return title[:50]


if __name__ == "__main__":
    pass

# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class TubousSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('tubous.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/tubous.png',
                              # menu_items=menu_items,
                              url=URL("https://www.tubous.com/", test_string='Porn'))

    def get_shrink_name(self):
        return 'TB'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'class':'thumbs'})
        # pretty(contents)
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'th'})):

                # pretty(thumbnail)
                xref=thumbnail.find('a',href=True)
                img=thumbnail.find('img')
                href = URL(xref.attrs['href'], base_url=url)
                img_url=img.attrs.get('data-src',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                title = thumbnail.find('p', {'class': 'video-title'})
                label = '' if title is None else collect_string(title)

                duration = thumbnail.find('span', {'class': 'dur'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_tag = thumbnail.find('span', {'class': 'quality'})
                hd = '' if hd_tag is None else collect_string(hd_tag)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])



    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        for container in _iter(soup.find_all('ul',{'class':'category'})):
            for item in _iter(container.find_all('a',href=lambda x:'/category/' in str(x))):
                # pretty(item)
                self.add_tag(collect_string_to_array(item)[0], URL(item.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            # pretty(container)
            data_current_page=container.attrs.get('data-current-page','1')
            data_duration = container.attrs.get('data-duration', '')
            data_max_page = container.attrs.get('data-max-page', '')
            data_niche_slug = container.attrs.get('data-niche-slug', '')
            data_paging_order = container.attrs.get('data-paging-order', '')
            data_q = container.attrs.get('data-q', '')
            if data_q:
                data_q='search/'+data_q

            # if data_q:
            #     psp(data_q)

            curr_page=int(data_current_page)

            if curr_page-5>1:
                self.add_page('1',URL('/'+data_niche_slug+data_paging_order+data_q+data_duration+'/page'+'1'+'.html',base_url=url))

            for page in range(curr_page-5,curr_page+5):
                if page>0 and page<=int(data_max_page):
                    if page==curr_page: continue
                    page_url=URL('/'+data_niche_slug+data_paging_order+data_q+data_duration+'/page'+str(page)+'.html',base_url=url)
                    # print(page_url)
                    self.add_page(str(page),page_url)

            if curr_page+5<=int(data_max_page):
                self.add_page(data_max_page,URL('/'+data_niche_slug+data_paging_order+data_q+data_duration+'/page'+data_max_page+'.html',base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagingContainer'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'watch'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'data-videolink' in str(x))
            # psp(script)

            data = str(script).replace(' ', '')
            if data:
                # psp(flashvars)

                video_url = quotes(data, 'data-videolink="', '"')
                # video_url_text = quotes(flashvars, 'data-videolink="', '"')
                if video_url:
                    self.add_video('default', URL(video_url, base_url=url))

                video_alt_url = quotes(data, 'data-mobile-videolink="', '"')
                if video_alt_url:
                    self.add_video('mobile', URL(video_alt_url, base_url=url))

            # for source in _iter(video.find_all('source')):
            #     # psp(source)
            #     if 'http' in source.attrs.get('src',''):
            #         self.add_video(source.attrs.get('title','default'), URL(source.attrs['src']))
            #     self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        container = soup.find('div', {'class': 'tr-desrc-other'})
        if container:
            for item in _iter(container.find_all('a', href=True)):
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

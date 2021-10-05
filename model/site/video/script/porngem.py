# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PorngemSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('porngem.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface): #
        # menu_items=dict(Top_Rated_Video=URL('https://pornone.com/rating/'),
        #             Latest_Video=URL('https://pornone.com/newest/'),
        #             Most_Viewed=URL('https://pornone.com/views/'),
        #             Longest_Video=URL('https://pornone.com/longest/'),
        #             HD_video=URL('https://pornone.com/newest/hd/'))

        view.add_start_button(picture_filename='model/site/resource/porngem.png',
                              # menu_items=menu_items,
                              url=URL("https://www.porngem.com/latest-updates/1/", test_string='porn'))

    def get_shrink_name(self):
        return 'PG'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents=soup.find('div', {'id':['list_videos_latest_videos_list_items',
                                         'list_videos_common_videos_list_items',
                                         'list_videos_model_videos_items']})
        # pretty(contents)
        if contents:
            # pretty(contents)
            for thumbnail in _iter(contents.find_all('div', {'class': 'item'})):

                # print(thumbnail)
                xref=thumbnail.find('a', href=True)
                img=thumbnail.find('img')
                # print(img)
                href = URL(xref.attrs['href'], base_url=url)
                img_url=img.attrs.get('data-original',thumbnail.img.attrs.get('src',''))
                thumb_url = URL(img_url, base_url=url)

                title_tag = thumbnail.find('strong', {'class': 'title'})
                # label = img.attrs.get('alt')
                label = img.attrs.get('alt') if title_tag is None else collect_string(title_tag)

                duration = thumbnail.find('span', {'class': 'duration-value'})
                dur_time = '' if duration is None else collect_string(duration)
                # dur_time = hd=quotes(str(thumbnail),'duration">','<')

                # hd_tag = thumbnail.find('span', {'class': 'hd-label'})
                # hd = '' if hd_tag is None else collect_string(hd_tag)
                hd=quotes(str(thumbnail),'hd-label">','<')

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       # {'text': count, 'align': 'top right'},
                                       {'text':label, 'align':'bottom center'},
                                       {'text': hd, 'align': 'top left'}])


    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            # pretty(container)
            if url.get().rstrip('/').rpartition('/')[2].isdigit():
                page_url_base=url.get().rstrip('/').rpartition('/')[0]+'/'
            else:
                page_url_base = url.get().rstrip('/') + '/'
            for page in _iter(container.find_all('a', {'data-parameters': True, 'class':['page', 'last']})):
                # pretty(page)
                pagenum=page.attrs.get('data-parameters').rpartition(':')[2]
                page_url=page_url_base+pagenum+'/'

                # print(page_url, pagenum)
                self.add_page(pagenum, URL(page_url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination-block'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video:
            # pretty(video)
            script=video.find('script',text=lambda x: 'flashvars' in str(x))
            # psp(script)

            flashvars = quotes(str(script).replace(' ', ''), 'flashvars={', '}')
            if flashvars:
                # psp(flashvars)

                video_url = quotes(flashvars, "video_url:'", "'")
                video_url_text = quotes(flashvars, "video_url_text:'", "'")
                # psp(video_url,video_url_text)

                video_alt_url = quotes(flashvars, "video_alt_url:'", "'")
                video_alt_url_text = quotes(flashvars, "video_alt_url_text:'", "'")

                video_alt_url2 = quotes(flashvars, "video_alt_url2:'", "'")
                video_alt_url2_text = quotes(flashvars, "video_alt_url2_text:'", "'")

                if video_url: self.add_video(video_url_text, URL(video_url, base_url=url, redirect=False))
                if video_alt_url: self.add_video(video_alt_url_text, URL(video_alt_url, base_url=url, redirect=False))
                if video_alt_url2: self.add_video(video_alt_url2_text, URL(video_alt_url2, base_url=url, redirect=False))

            # for source in _iter(video.find_all('source')):
            #     # psp(source)
            #     if 'http' in source.attrs.get('src',''):
            #         self.add_video(source.attrs.get('title','default'), URL(source.attrs['src']))
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'additional-description'})

        if container:
            # pretty(container)
            for item in _iter(container.find_all('a', href=lambda x:'/models/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url), style=dict(color='red'))

            for item in _iter(container.find_all('a', href=lambda x:'/categories/' in str(x))):
                # pretty(item)
                href = item.attrs.get('href', '')
                self.add_tag(collect_string(item), URL(href, base_url=url))

            for item in _iter(container.find_all('a', href=lambda x:'/tags/' in str(x))):
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

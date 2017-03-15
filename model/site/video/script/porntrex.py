# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PorntrexSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('porntrex.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items= {
            'Categories' : URL('http://www.porntrex.com/categories/'),
            'Top rated'  : URL('http://www.porntrex.com/top-rated/'),
            'Most viewed': URL('http://www.porntrex.com/most-popular/'),
            'Latest'     : URL('http://www.porntrex.com/latest-updates/')
        }

        view.add_start_button(picture_filename='model/site/resource/porntrex.png',
                              menu_items=menu_items,
                              url=URL("http://www.porntrex.com/latest-updates/"))

    def get_shrink_name(self):
        return 'PT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'video-item'})):
            private=thumbnail.find('span',{'class':'ico-private'})
            if not private:
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                description = thumbnail.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['data-original'], base_url=url)

                duration = thumbnail.find('div', {'class': 'durations'})
                dur_time = '' if duration is None else str(duration.contents[-1]).strip()

                hd_div = thumbnail.find('div', {'class': 'hd-text-icon'})
                hd = '' if hd_div is None else str(hd_div.string).strip()

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'},
                                       {'text': hd, 'align': 'top left', 'bold': True}])


    def parse_others(self, soup: BeautifulSoup, url: URL):
        # Categories page
        categories=dict()
        for thumbs_container in _iter(soup.find_all('div', {'class': 'list-categories'})):
            for thumbnail in _iter(thumbs_container.find_all('a',{'class':'item'})):
                href = URL(thumbnail.attrs['href'], base_url=url)
                description = thumbnail.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                no = thumbnail.find('div', {'class': 'videos'})
                no_of_video = '' if no is None else str(no.string).strip()

                categories[description]=(href,thumb_url,no_of_video)

        for description in sorted(categories):
            (href, thumb_url, no_of_video)=categories[description]

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                            labels=[{'text': no_of_video, 'align': 'top right'},
                                    {'text': description, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        for tags_container in _iter(soup.find_all('div', {'class': 'sidebar'})):
                for tag in _iter(tags_container.find_all('a', href=lambda x:'/categories/' in str(x))):
                    self.add_tag(str(tag.contents[0]), URL(tag.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'pagination-holder'})
        if container is not None:
            for page in container.find_all('a', {'href': True}):
                if page.string and page.string.isdigit():
                    href=page.attrs['href']
                    if '#videos' in href:
                        # "bypass" to Ajax
                        #  http://www.porntrex.com/categories/big-tits/?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=post_date&from=08
                        url_txt=url.get().strip('/')
                        part=url_txt.rpartition('/')

                        if part[2].isdigit():
                            url_txt=part[0]

                        self.add_page(page.string, URL(url_txt + '/'+ page.string+'/'))
                    else:
                        self.add_page(page.string, URL(page.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'class': 'player'})
        if content is not None:
            script =content.find('script', text=lambda x: 'flashvars =' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\n', '').replace('\t', '')
                flashvars = quotes(data,'flashvars={', '};').split(',')
                fv = dict()
                for flashvar in flashvars:
                    split = flashvar.partition(':')
                    fv[split[0]] = split[2].strip("'\"")
                files = dict()
                for f in fv:
                    if fv[f].startswith('http://') and fv[f].endswith('.mp4/'):
                        file = fv[f]
                        label = fv.get(f + '_text', f)
                        files[label] = file

                for key in sorted(files.keys(), reverse=True):
                    self.add_video(key, URL(files[key]))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # adding user to video
        user_container = soup.find('div', {'class': 'username'})
        href = URL(user_container.a.attrs['href'] + 'videos/', base_url=url)
        username = str(user_container.a.string).strip()
        self.add_tag(username, href, style=dict(color='blue'))

        # adding tags to video
        for item in _iter(soup.find_all('div', {'class': 'info'})):
            for href in _iter(item.find_all('a', href=lambda x:'/categories/' in str(x) )):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass

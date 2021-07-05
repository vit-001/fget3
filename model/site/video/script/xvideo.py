# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string, pretty

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class XvideoSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('xvideos.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items={'Pornstars':URL('http://www.xvideos.com/pornstars*'),  #http://www.xvideos.com/channels
                    'Russian Pornstars': URL('http://www.xvideos.com/pornstars/russia*'),
                    'Pornstars ever': URL('http://www.xvideos.com/pornstars/ever*'),
                    'Channels': URL('http://www.xvideos.com/channels*'),
                    'New video': URL('http://www.xvideos.com/'),
                    }

        view.add_start_button(picture_filename='model/site/resource/xvideos.gif',
                              menu_items=menu_items,
                              url=URL("http://www.xvideos.com/", test_string='XVIDEOS.COM'))

    def get_shrink_name(self):
        return 'XV'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        suffix=''
        if url.contain('/channels'):
            suffix = '/videos/new/0'
        elif url.contain('/pornstars'):
            suffix='/videos/pornstar/0'

        if url.contain('/pornstar-channels/'):
            sub=soup.find('div', {'class':'tabVideos'})
            pretty(sub)


        container=soup.find('div', {'class': 'mozaique'})
        if container:
            # pretty(container)
            
            for item in _iter(soup.find_all('div', {'class': 'thumb-block'})):
                # pretty(item)
                inside=item.find('div', {'class': 'thumb-inside'})
                under=item.find('div', {'class': 'thumb-under'})
                # pretty(inside)
                # pretty(under)

                href=under.find('a')
                xref_url = URL(href.attrs['href'], base_url=url)
                label = href.attrs['title']

                # script=thumbnail.script.string
                # thumb_url = URL(quotes(script,'src="','"'), base_url=url)
                thumb_url = URL(inside.img.attrs['data-src'], base_url=url)

                duration = under.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else str(duration.string)

                # hd_span = thumbnail.find('span', {'class': 'video-hd-mark'})
                # hd = '' if hd_span is None else str(hd_span.string)

                self.add_thumb(thumb_url=thumb_url, href=xref_url, popup=label,
                               labels=[{'text':dur_time, 'align':'top right'},
                                       {'text':label, 'align':'bottom center'}])
        #
        # for thumbnail in _iter(soup.find_all('div', {'class': 'thumb-block'})):
        #     # psp(thumbnail.prettify())
        #     href=thumbnail.find('a',
        #                         title=True,
        #                         href=lambda x: str(x).startswith('/video') or str(x).startswith('/prof-video-click/'))
        #
        #     profiles=thumbnail.find('p',{'class':'profile-name'})
        #     if href:
        #         xref_url = URL(href.attrs['href'], base_url=url)
        #         label = href.attrs['title']
        #
        #         # script=thumbnail.script.string
        #         # thumb_url = URL(quotes(script,'src="','"'), base_url=url)
        #         thumb_url = URL(thumbnail.img.attrs['data-src'], base_url=url)
        #
        #         duration = thumbnail.find('span', {'class': 'duration'})
        #         dur_time = '' if duration is None else str(duration.string)
        #
        #         hd_span = thumbnail.find('span', {'class': 'video-hd-mark'})
        #         hd = '' if hd_span is None else str(hd_span.string)
        #
        #         self.add_thumb(thumb_url=thumb_url, href=xref_url, popup=label,
        #                        labels=[{'text':dur_time, 'align':'top right'},
        #                                {'text':label, 'align':'bottom center'},
        #                                {'text': hd, 'align': 'top left'}])
        #
        #     if profiles:
        #         xref_url = URL(profiles.a.attrs['href'] + suffix, base_url=url)
        #         label = str(profiles.a.string).strip()
        #
        #         script=thumbnail.script.string
        #         thumb_url = URL(quotes(script,'src="','"'), base_url=url)
        #
        #         count = thumbnail.find('p',{'class': 'profile-counts'})
        #         videos = '' if count is None else str(count.string).strip()
        #
        #         flag_span = thumbnail.find('span', {'class': 'flag'})
        #         flag = '' if flag_span is None else str(flag_span.attrs['title'])
        #
        #         self.add_thumb(thumb_url=thumb_url, href=xref_url, popup=label,
        #                        labels=[{'text':videos, 'align':'top right'},
        #                                {'text':label, 'align':'bottom center'},
        #                                {'text': flag, 'align': 'top left'}
        #                                ])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'main-categories'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a',href=True)):
                xref=tag.attrs['href']
                if xref != '/tags':
                    self.add_tag(collect_string(tag), URL(xref, base_url=url))
            script=tags_container.find('script', text=lambda x: 'url' in str(x))
            if script:
                temp=quotes(script.text.replace('\\',''),'cats.write([{','}]').split('},{')
                for item in temp:
                    href=quotes(item,'"url":"','"')
                    label=quotes(item,'"label":"','"')
                    if href and label:
                        self.add_tag(label,URL(href,base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and page.string.isdigit():
                    xref=str(page.attrs['href'])
                    if xref.startswith('#'):
                        page_url=URL(xref.strip('#'), base_url=url)
                    else:
                        page_url= URL(xref, base_url=url)
                    self.add_page(page.string, page_url)

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'video-player-bg'})
        if video:
            # psp(video)
            script=video.find('script', text=lambda x: 'HTML5Player' in str(x))
            if script is not None:
                lines=str(script.string).split(';')
                for line in lines:
                    if line.strip().startswith('html5player.setVideoUrl'):
                        label=quotes(line,'setVideoUrl','(')
                        href= URL(quotes(line, "'", "'"))
                        self.add_video(label, href)
                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # adding "user" and "star" to video
        container=soup.find('div', {'class': 'video-metadata'})
        pretty(container)
        if container:
            # for metadata in _iter(soup.find_all('div', {'class': 'video-metadata'})):
            #     # pretty(metadata)
            #     uploader=metadata.find('span', {'class','uploader'})
            #     if uploader:
            #         hlink=uploader.a
            #         self.add_tag(str(hlink.string), URL(hlink.attrs['href']+'/videos/new/0', base_url=url), style=dict(color='blue'))
            #     if 'Models ' in str(metadata):
            #         for href in _iter(metadata.find_all('a', href=lambda x: '/profiles/' in str(x))):
            #             self.add_tag(str(href.string),
            #                          URL(href.attrs['href'] + '/videos/pornstar/0', base_url=url),
            #                          style=dict(color='red'))

            # adding "tags" to video
            # for tag in _iter(soup.find_all('a', {'class': 'video-metadata'})):

            for href in _iter(container.find_all('a', href=lambda x: '/profiles/' in str(x))):
                xref=href.attrs['href']
                name=href.find('span', {'class': 'name'})
                # if xref != '/tags/':
                self.add_tag(str(name.string), URL(xref, base_url=url), style=dict(color='blue'))

            for href in _iter(container.find_all('a', href=lambda x: '/pornstar-channels/' in str(x))):
                xref=href.attrs['href']+'#_tabVideos*'
                name=href.find('span', {'class': 'name'})
                # if xref != '/tags/':
                self.add_tag(str(name.string), URL(xref, base_url=url),style=dict(color='red'))

            for href in _iter(container.find_all('a', href=lambda x: '/tags/' in str(x))):
                xref=href.attrs['href']
                if xref != '/tags/':
                    self.add_tag(str(href.string), URL(xref, base_url=url))

if __name__ == "__main__":
    pass

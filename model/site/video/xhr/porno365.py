# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
from copy import copy
from json import loads, dumps

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class Porno365Site(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('porno365.sex/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        # menu_items=dict(Longest=URL('http://www.extremetube.com/videos?o=lg*'),
        #             Most_popular=URL('http://www.extremetube.com/videos?o=mv*'),
        #             Latest=URL('http://www.extremetube.com/videos*'),
        #             Top_Rated=URL('http://www.extremetube.com/videos?o=tr*'),
        #             Categories=URL('http://www.extremetube.com/video-categories*'))

        view.add_start_button(picture_filename='model/site/resource/porno365.png',
                              # menu_items=menu_items,
                              url=URL("http://porno365.sex/", test_string='Porno365'))

    def get_shrink_name(self):
        return '365'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):

        if not url.any_data:
            container=soup.find('div',{'id':'video-content'})
            if container:
                # psp(container)
                for thumbnail in _iter(container.find_all('li', {'class': 'video_block'})):
                    # psp(thumbnail.prettify())
                    xref=thumbnail.find('a')
                    if xref:
                        # psp(xref.prettify())
                        href = URL(xref.attrs['href'], base_url=url)
                        thumb_url = URL(xref.img.attrs['src'], base_url=url)
                        label=thumbnail.img.attrs.get('alt','')

                        duration = thumbnail.find('span', {'class': 'duration'})
                        dur_time = str(duration.contents[-1]) if duration else ''
                        # dur_time=xref.attrs['data-duration']

                        # hd_span = thumbnail.find('span', {'class': 'text-active bold'})
                        # hd = '' #if hd_span is None else str(hd_span.string)

                        self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                       labels=[{'text':dur_time, 'align':'top right'},
                                               {'text':label, 'align':'bottom center'},
                                               #{'text': hd, 'align': 'top left'}
                                                ])
        else:
            # psp(url.any_data)
            self.waiting_data=True
            self._result_type = 'thumbs'

            json_file_url=url.any_data['json_file_url']
            json_file_url.any_data=dict(first_page_url=url)

            filedata = FLData(json_file_url, '')
            self.model.loader.start_load_file(filedata, self.parse_thumbs_json)

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        if url.any_data:
            label=self.get_thumb_label(url.any_data['json_file_url'])
            spl=label.partition('?')
            short= spl[0]+' p'+spl[2].partition('page=')[2]
            return self.get_shrink_name().strip() + ' ' + short
        else:

            return self.get_shrink_name().strip() + ' ' + self.get_thumb_label(url)

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        # psp()
        # print('========PAGINATION=========')
        # print(url.get())
        base=url.get().partition('page-')[0]
        if base[-1]!='/' and base[-1]!='-':
            base=base+'-'
        # print(base)

        current_page=quotes(url.get(),'page-','.html')
        if current_page:
            self.add_page('1', URL(base + 'page-1.html'))
        else:
            current_page='1'

        no=int(current_page)

        for pno in range(no-5,no+5):
            if pno < 2: continue
            if pno == no: continue
            self.add_page(str(pno), URL(base + 'page-{0}.html'.format(pno)))

        psp()

    #
    # def parse_others(self, soup: BeautifulSoup, url: URL):
    #     container=soup.find('div',{'class':'categories-list-thumb'})
    #     if container:
    #         for xref in _iter(container.find_all('a', href=lambda x: '/category/' in str(x))):
    #             href = URL(xref.attrs['href'], base_url=url)
    #             thumb_url = URL(xref.img.attrs['src'], base_url=url)
    #             label = xref.img.attrs.get('alt', '')
    #
    #             self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
    #                            labels=[{'text': label, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'menu_inner'})
        if tags_container:
            # psp(tags_container)
            for tag in _iter(tags_container.find_all('a')):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'player_div'})
        if video is not None:
            script=soup.find('script', text=lambda x: 'jwplayer("player_div").setup' in str(x))
            if script:
                data = str(script.string).replace('\t', '')#.replace('\n', '')#.replace(' ', '')
                sources = quotes(data,'sources: [{', '}]').split('},{')
                for source in sources:
                    # psp(source)
                    file= quotes(source,'file: "','"')
                    label = quotes(source, 'label: "', '"')

                    self.add_video(label,URL(file))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'video_extras'})


        for categories in _iter(container.find_all('div', {'class':'video-categories'})):
            # psp(categories.prettify())

            for xref in _iter(categories.find_all('a')):
                if 'suggest_model' in xref.attrs['href']: continue

                color='black'

                if '/models/' in xref.attrs['href']:
                    color='red'

                psp(xref)

                print(str(xref.string), URL(xref.attrs['href'], base_url=url))
                self.add_tag(str(xref.string), URL(xref.attrs['href'], base_url=url), style=dict(color=color))


if __name__ == "__main__":
    pass

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


class ExtremetubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('extremetube.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Longest=URL('http://www.extremetube.com/videos?o=lg*'),
                    Most_popular=URL('http://www.extremetube.com/videos?o=mv*'),
                    Latest=URL('http://www.extremetube.com/videos*'),
                    Top_Rated=URL('http://www.extremetube.com/videos?o=tr*'),
                    Categories=URL('http://www.extremetube.com/video-categories*'))

        view.add_start_button(picture_filename='model/site/resource/extremetube.png',
                              menu_items=menu_items,
                              url=URL("http://www.extremetube.com/videos", test_string='porno'))

    def get_shrink_name(self):
        return 'ET'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):

        if not url.any_data:
            container=soup.find('ul',{'class':'videoList'})
            if container:
                for thumbnail in _iter(container.find_all('div', {'class': 'video-box-wrapper'})):
                    # psp(thumbnail.prettify())
                    xref=thumbnail.find('a')
                    if xref:
                        # psp(xref.prettify())
                        href = URL(xref.attrs['href'], base_url=url)
                        thumb_url = URL(xref.img.attrs['data-srcmedium'], base_url=url)
                        label=thumbnail.img.attrs.get('alt','')

                        # duration = thumbnail.find('span', {'class': 'fs11 viddata flr'})
                        # dur_time = '' if duration is None else str(duration.contents[-1])
                        dur_time=xref.attrs['data-duration']

                        # hd_span = thumbnail.find('span', {'class': 'text-active bold'})
                        hd = '' #if hd_span is None else str(hd_span.string)

                        self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                       labels=[{'text':dur_time, 'align':'top right'},
                                               {'text':label, 'align':'bottom center'},
                                               {'text': hd, 'align': 'top left'}])
        else:
            # psp(url.any_data)
            self.waiting_data=True
            self._result_type = 'thumbs'

            json_file_url=url.any_data['json_file_url']
            json_file_url.any_data=dict(first_page_url=url)

            filedata = FLData(json_file_url, '')
            self.model.loader.start_load_file(filedata, self.parse_thumbs_json)


    def parse_thumbs_json(self, fldata:FLData):
        data=loads(fldata.text)
        if type(data)==dict:
            page=data['1']
        elif type(data)==list:
            page=data[0]
        else:
            page=None

        try:
            items=page['items']
            for item in items:
                href=URL(item['video_link'],base_url=fldata.url)
                label=item['title_long']
                dur_time=item['duration']
                thumb_url=URL(item['thumb_url'],base_url=fldata.url)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'}])

            # create pagination
            navigation=page['navigation']
            last_page=navigation['lastPage']
            current=navigation['currentPage']
            pattern=navigation['urlPattern'].replace('[%pageId%]','{0}')

            for page_no in range(current-5,current+5):

                if page_no==current: continue
                if page_no<3: continue
                if page_no>last_page: continue

                page_url=URL(fldata.url.any_data['first_page_url'].get())
                page_url.any_data=dict(json_file_url=URL(pattern.format(page_no),base_url=fldata.url))

                self.add_page(str(page_no), page_url)

            # add last page
            page_url = URL(fldata.url.any_data['first_page_url'].get())
            page_url.any_data = dict(json_file_url=URL(pattern.format(last_page), base_url=fldata.url))

            self.add_page(str(last_page), page_url)

        except TypeError as err:
            print(dumps(data, sort_keys=True, indent=4))
            print('Error:', err)

        self.waiting_data=False
        self.generate_thumb_view()

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        if url.any_data:
            label=self.get_thumb_label(url.any_data['json_file_url'])
            spl=label.partition('?')
            short= spl[0]+' p'+spl[2].partition('page=')[2]
            return self.get_shrink_name().strip() + ' ' + short
        else:

            return self.get_shrink_name().strip() + ' ' + self.get_thumb_label(url)

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        first_page=URL(url.get())
        self.add_page('1', first_page)

        next_link=soup.find('link', {'rel':'next'})
        if next_link:
            json_file_href=next_link.attrs['href'].replace('page=','format=json&number_pages=1&page=')
            json_file_url=URL(json_file_href,base_url=url)
            page=json_file_href.rpartition('page=')[2]

            old_url=copy(url)
            old_url.any_data=dict(json_file_url=json_file_url)
            self.add_page(page, old_url)

    def parse_others(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'categories-list-thumb'})
        if container:
            for xref in _iter(container.find_all('a', href=lambda x: '/category/' in str(x))):
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(xref.img.attrs['src'], base_url=url)
                label = xref.img.attrs.get('alt', '')

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': label, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('select', {'class': 'js_categoriesSelector'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('option', value=lambda x: '/category/' in str(x))):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['value'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'video-container'})
        if video is not None:
            script=video.find('script', text=lambda x: 'flashvars' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\t', '').replace('\n', '')
                flashvars = quotes(data,'flashvars={', '};').split(',')
                for flashvar in flashvars:
                    if flashvar.startswith('"quality_'):
                        split = flashvar.partition('":"')
                        self.add_video(split[0],URL(split[2].rstrip('"').replace('\\/','/'),base_url=url))

                self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'infoBlock'})
        # psp(container.prettify())

        owner=container.find('a',{'class':'owner'})
        if owner:
            # psp(owner)
            self.add_tag(str(owner.string),URL(owner.attrs['href'],base_url=url),style=dict(color='blue'))

        filename=container.find('div', {'class':'ibTrigger'})
        info_url=URL('/details/'+filename.attrs['data-slug'],base_url=url)

        self.waiting_data=True

        filedata = FLData(info_url, '')

        self.model.loader.start_load_file(filedata, self.continue_parse_video_tags)


    def continue_parse_video_tags(self, fldata:FLData):
        # print(fldata.text)
        soup=BeautifulSoup(fldata.text,'html.parser')
        # psp(soup.prettify())

        for data in _iter(soup.find_all('div',{'class':'ibData'})):
            for xref in _iter(data.find_all('a')):
                # psp(xref)
                href=URL(xref.attrs['href'],base_url=fldata.url)
                if href.contain('/pornstar/'):
                    style = dict(color='red')
                else:
                    style = None

                self.add_tag(str(xref.string),href, style=style)

        self.waiting_data=False
        self.generate_video_view()


if __name__ == "__main__":
    pass

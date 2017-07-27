# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string, sp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PervertslutSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pervertslut.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Categories=URL('http://pervertslut.com/categories/'),
                    Latest=URL('http://pervertslut.com/latest-updates/'),
                    TopRated=URL('http://pervertslut.com/top-rated/'),
                    MostViewed=URL('http://pervertslut.com/most-popular/'))

        view.add_start_button(picture_filename='model/site/resource/pervertslut.png',
                              menu_items=menu_items,
                              url=URL("http://pervertslut.com/latest-updates/", test_string='porn'))

    def get_shrink_name(self):
        return 'PL'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        if not url.any_data:
            self._parse_thumbs(soup,url)
        else:
            self.waiting_data = True
            self._result_type = 'thumbs'

            xhr_url=url.any_data['xhr']
            xhr_url.any_data=dict(base=url)
            filedata = FLData(url.any_data['xhr'], '')
            self.model.loader.start_load_file(filedata, self.parse_thumbs_xhr)

    def parse_thumbs_xhr(self, fldata: FLData):
        # psp(fldata.url, fldata.url.any_data)
        soup=BeautifulSoup(fldata.text,'html.parser')
        # psp(soup.prettify())

        self._parse_thumbs(soup,fldata.url.any_data['base'])

        # self._parse_pagination(soup,fldata.url.any_data['base'])

        self.waiting_data=False
        self.generate_thumb_view()

    def _parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'item'})):
            # psp(thumbnail.prettify())
            xref = thumbnail.find('a')
            if xref:
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                label = thumbnail.img.attrs.get('alt', '')

                duration = thumbnail.find('div', {'class': 'duration-overlay'})
                dur_time = '' if duration is None else collect_string(duration)

                hd_span = thumbnail.find('span', {'class': 'hd'})
                hd = '' if hd_span is None else str(hd_span.string).strip()

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'},
                                       {'text': hd, 'align': 'top left'}])

        self._parse_pagination(soup, url)

    def parse_others(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'list-categories'})
        if container:
            for xref in _iter(container.find_all('a', {'class':'item'})):
                href = URL(xref.attrs['href'], base_url=url)
                thumb_url = URL(xref.img.attrs['src'], base_url=url)
                label = xref.img.attrs.get('alt', '')

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': label, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'sidebar'})
        if tags_container:
            for tag in _iter(tags_container.find_all('a',{'href':lambda x: '/categories/' in x})):
                self.add_tag(collect_string(tag).rstrip('.0123456789'), URL(tag.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        pass

    def _parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div', {'class': 'pagination-holder'})
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if not page.attrs['href'].startswith('#'):
                    self.add_page(page.string, URL(page.attrs['href'], base_url=url))
                else:
                    pair_list=[('mode','async'),
                               ('function','get_block'),
                               ('block_id', page.attrs['data-block-id'])]
                    parameters=page.attrs['data-parameters'].split(';')
                    for item in parameters:
                        key,unused,value=item.partition(':')
                        pair_list.append(tuple([key,value]))

                    xhr_url=URL(url.get())
                    xhr_url.add_query(pair_list)
                    page_url=URL(url.get())
                    page_url.any_data=dict(xhr=xhr_url)

                    self.add_page(page.string, page_url)


    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'player'})
        if video is not None:
            # psp(video.prettify())
            script=video.find('script', text=lambda x: 'video_url:' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')#.replace('\t', '').replace('\n', '')
                # psp(data)
                mp4=quotes(data,"video_url:'","'")
                self.add_video('DEFAULT', URL(mp4, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().rpartition('/')[0].rpartition('/')[2]

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'info'})
        if container:
            for xref in _iter(container.find_all('a')):
                href=URL(xref.attrs['href'],base_url=url)
                self.add_tag(str(xref.string),href)

if __name__ == "__main__":
    pass

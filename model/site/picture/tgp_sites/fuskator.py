# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
from urllib.parse import unquote

from common.util import _iter, quotes, psp
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.picture.base_of_tgp import TgpSite


class FuskatorSite(TgpSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('fuskator.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Rating_Sort=URL('http://fuskator.com/search/-/rating/'),
                        Quality_Sort=URL('http://fuskator.com/search/-/quality/'),
                        Unsorted=URL('http://fuskator.com/'),
                        Tags_Sort=URL('http://fuskator.com/search/-/tags/'),
                    )

        view.add_start_button(picture_filename='model/site/resource/picture/fuskator.png',
                              menu_items=menu_items,
                              url=URL("http://fuskator.com/", test_string='Fuskator'))

    def get_shrink_name(self):
        return 'FK'

    def get_thumbs_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div', {'class':'thumblinks'})

    def get_thumbs_from_container(self, container: BeautifulSoup) -> list:
        return container.find_all('div',{'class':'pic'})

    def parse_one_thumb(self, thumbnail:BeautifulSoup, url:URL):
        xref=thumbnail.find('a', href=True)
        if xref:
            href = URL(xref.attrs['href'],base_url=url)

            description = xref.img.attrs.get('alt', '')
            thumb_url = URL(xref.img.attrs['src'], base_url=url)
            data=thumbnail.find('div',{'class':'gallery_data'})
            pics=str(data.string).partition('/')[0] if data else ''

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                           labels=[{'text': description, 'align': 'bottom center'},
                                   {'text': pics, 'align': 'top right'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('td',{'class':'pages'})

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class':'imagelinks'})
        if container:
            # psp(container.prettify())
            base=''
            for item in _iter(container.find_all('script')):
                script=str(item.string).strip()
                # psp(script)
                if script.startswith('var '):
                    base=unquote(quotes(script,"'","'"))
                    # psp(base)
                else:
                    suffix=quotes(script,"+'","'")
                    image_url=URL(base+suffix)
                    # psp(pic_url)
                    # image_url=self.get_image_url(image, url)
                    filename=self.get_image_filename(image_url)
                    self.add_picture(filename,image_url)

    def get_picture_tag_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div',id='divTags')


if __name__ == "__main__":
    pass
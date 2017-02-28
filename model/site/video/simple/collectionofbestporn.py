# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL

from model.site.base_site import BaseSite,AbstractViewFromModelInterface, BeautifulSoup

class CollectionofbestpornSite(BaseSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('collectionofbestporn.com/')

    @staticmethod
    def create_start_button(view:AbstractViewFromModelInterface):
        view.add_start_button(name='Collectionofbestporn',
                              picture_filename='',
                              url=URL("http://collectionofbestporn.com/most-recent*", test_string='Collection'))


    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        thumbs=soup.find_all('div', {'class': 'video-thumb'})
        if thumbs:
            view=self.prepare_thumb_view()
            for thumbnail in thumbs:
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                description = thumbnail.a.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                duration = thumbnail.find('span', {'class': "time"})
                dur_time = '' if duration is None else str(duration.string)

                quality = thumbnail.find('span', {'class': "quality"})
                qual = '' if quality is None else str(quality.string)

                view.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text': dur_time, 'align': 'top right'},
                                                   {'text': description, 'align': 'bottom center'},
                                                   {'text': qual, 'align': 'top left', 'bold': True}])


if __name__ == "__main__":
    pass
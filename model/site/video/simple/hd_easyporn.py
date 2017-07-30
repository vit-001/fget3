__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class HdEasypornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('hd-easyporn.com/')

    @staticmethod
    def create_start_button(view: ViewManagerFromModelInterface):
        menu_items=dict(Videos_Newest=URL('http://www.hd-easyporn.com/?o=n*'),
                    Videos_Most_Viewed=URL('http://www.hd-easyporn.com/?o=v*'),
                    Videos_Top_Rated=URL('http://www.hd-easyporn.com/?o=r*'),
                    Videos_Longest=URL('http://www.hd-easyporn.com/?o=d*'),
                    Categories=URL('http://www.hd-easyporn.com/categories/')
                    )

        view.add_start_button(picture_filename='model/site/resource/hd_easyporn.png',
                              menu_items=menu_items,
                              url=URL("http://www.hd-easyporn.com/", test_string='HD Porn'))


    def get_shrink_name(self):
        return 'HDEP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        thumbs_container = soup.find('div', {'class': 'videos cf'})
        if thumbs_container is not None:
            for thumbnail in _iter(thumbs_container.find_all('div', {'class': ['polaroid']})):
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                description = thumbnail.a.img.attrs['alt']
                thumb_url = URL(thumbnail.img.attrs['data-src'], base_url=url)

                duration = thumbnail.find('div', {'class': "duration"})
                dur_time = '' if duration is None else str(duration.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                           labels=[{'text': dur_time, 'align': 'top right'},
                                                   {'text': description, 'align': 'bottom center'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        categories = set()
        for category in _iter(soup.find_all('div', {'class': 'catbox'})):
            href = URL(category.a.attrs['href'], base_url=url)
            thumb_url = URL(category.img.attrs['data-src'], base_url=url)
            title = str(category.find('div', {'class': 'title'}).string)

            if title not in categories:
                self.add_thumb(thumb_url=thumb_url, href=href, popup=title,
                                           labels=[{'text': title, 'align': 'top right'}])
                categories.add(title)

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pagination'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags = soup.find('ul', {'class': 'tags cf'})
        if tags is not None:
            for tag in tags.find_all('a'):
                self.add_tag(str(tag.string).strip(), URL(tag.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'class': 'video'})
        if video is not None:
            for source in _iter(video.find_all('source')):
                self.add_video(source.attrs['res'], URL(source.attrs['src'], base_url=url))
            self.set_default_video(-1)

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return super().parse_video_title(soup, url).rpartition('-')[0]

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for tag_container in _iter(soup.find_all('div', {'class': 'video_header'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass

__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.base_site import BaseSiteParser


class ShockingmoviesSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('shockingmovies.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(recent=URL('http://shockingmovies.com/most-recent/'),
                    most_viewed_week=URL('http://shockingmovies.com/most-viewed-week/'),
                    most_viewed_month=URL('http://shockingmovies.com/most-viewed-month/'),
                    most_viewed_all_time=URL('http://shockingmovies.com/most-viewed/'),
                    top_rated=URL('http://shockingmovies.com/top-rated/'),
                    longest=URL('http://shockingmovies.com/longest/'))

        view.add_start_button(name='Shockingmovies',
                              picture_filename='model/site/resource/shockingmovies.png',
                              menu_items=menu_items,
                              url=URL("http://shockingmovies.com/most-recent/", test_string='Shocking'))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('a', {'class': 'video-box'})):
            href = URL(thumbnail.attrs['href'], base_url=url)
            description = thumbnail.img.attrs['alt']
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

            duration = thumbnail.find('span', {'class': "video-length"})
            dur_time = '' if duration is None else str(duration.string)

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text': dur_time, 'align': 'top right'},
                                               {'text': description, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        for tag in _iter(soup.find_all('li', {'class': 'main-nav-item '})):
            href = tag.find('a', href=lambda x: '/channels/' in str(x))
            if href is not None:
                self.add_tag(str(href.string).strip(), URL(href.attrs['href'], base_url=url))

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'SM '+ url.get().partition('shockingmovies.com/')[2].partition('.')[0].strip('/')

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination-block'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        script = soup.find('script', text=lambda x: 'var urls' in str(x))
        if script is not None:
            self.add_video('DEFAULT', URL(quotes(str(script.string), 'file:"', '"'), base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().rpartition('/')[2].rpartition('.')[0].rpartition('-')[0]

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # adding "user" to video
        for item in _iter(soup.find_all('div', {'class': 'video-player-info'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string).strip(',\n').replace('/user/', '/uploads-by-user/'),
                                URL(href.attrs['href'], base_url=url), style={'color':'blue'})

        # adding tags to video
        for item in _iter(soup.find_all('div', {'class': 'tag-list-block'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string).strip(',\n'), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass

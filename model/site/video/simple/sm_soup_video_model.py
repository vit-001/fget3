__author__ = 'Vit'
from bs4 import BeautifulSoup

from base_classes import UrlList
from loader.base_loader import URL
from site_models.base_site_model import ParseResult, ControlInfo, ThumbInfo
from site_models.soup.base_soup_model import BaseSoupSite, _iter
from site_models.util import quotes


class SMvideoSoupSite(BaseSoupSite):
    def start_button_name(self):
        return "SMvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(recent=URL('http://shockingmovies.com/most-recent/'),
                    most_viewed_week=URL('http://shockingmovies.com/most-viewed-week/'),
                    most_viewed_month=URL('http://shockingmovies.com/most-viewed-month/'),
                    most_viewed_all_time=URL('http://shockingmovies.com/most-viewed/'),
                    top_rated=URL('http://shockingmovies.com/top-rated/'),
                    longest=URL('http://shockingmovies.com/longest/'))

    def startpage(self):
        return URL("http://shockingmovies.com/most-recent/", test_string='Shocking')

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('shockingmovies.com/')

    def parse_thumbs(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for thumbnail in _iter(soup.find_all('a', {'class': 'video-box'})):
            # psp(thumbnail.prettify())

            href = URL(thumbnail.attrs['href'], base_url=base_url)
            description = thumbnail.img.attrs['alt']
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=base_url)

            duration = thumbnail.find('span', {'class': "video-length"})
            dur_time = '' if duration is None else str(duration.string)

            result.add_thumb(ThumbInfo(thumb_url=thumb_url, href=href, popup=description,
                                       labels=[{'text': dur_time, 'align': 'top right'},
                                               {'text': description, 'align': 'bottom center'}]))

    def parse_thumbs_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        for tag in _iter(soup.find_all('li', {'class': 'main-nav-item '})):
            href = tag.find('a', href=lambda x: '/channels/' in str(x))
            if href is not None:
                result.add_control(ControlInfo(str(href.string).strip(), URL(href.attrs['href'], base_url=base_url)))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination-block'})

    def parse_video(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        script = soup.find('script', text=lambda x: 'var urls' in str(x))
        # psp(script)
        if script is not None:
            urls = UrlList()
            urls.add('DEFAULT', URL(quotes(str(script.string), 'file:"', '"'), base_url=base_url))
            result.set_video(urls.get_media_data())

    def parse_video_tags(self, soup: BeautifulSoup, result: ParseResult, base_url: URL):
        # adding "user" to video
        for item in _iter(soup.find_all('div', {'class': 'video-player-info'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    result.add_control(ControlInfo(str(href.string).strip(',\n').replace('/user/', '/uploads-by-user/'),
                                                   URL(href.attrs['href'], base_url=base_url), text_color='blue'))

        # adding tags to video
        for item in _iter(soup.find_all('div', {'class': 'tag-list-block'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    result.add_control(
                        ControlInfo(str(href.string).strip(',\n'), URL(href.attrs['href'], base_url=base_url)))


if __name__ == "__main__":
    pass

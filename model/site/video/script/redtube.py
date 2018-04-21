__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser


class RedtubeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('redtube.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Recommended=URL('http://www.redtube.com/recommended*'),
                    Newest=URL('http://www.redtube.com/'),
                    Top_Rated=URL('http://www.redtube.com/top*'),
                    Longest=URL('http://www.redtube.com/longest*'),
                    Most_Viewed_By_Week=URL('http://www.redtube.com/mostviewed*'),
                    Most_Favored_By_Week=URL('http://www.redtube.com/mostfavored*'),
                    Most_Viewed_All_Time=URL('http://www.redtube.com/mostviewed?period=alltime*'),
                    Most_Favored_All_Time=URL('http://www.redtube.com/mostfavored?period=alltime*'),
                    Pornstars=URL('http://www.redtube.com/pornstar/alphabetical*'),
                    Channels_Alphabetical=URL('http://www.redtube.com/channel/alphabetical*'),
                    Channels_Top_Rated=URL('http://www.redtube.com/channel/top-rated*'),
                    Channels_Recommended=URL('http://www.redtube.com/channel/recommended*'),
                    Channels_Recently_Updated=URL('http://www.redtube.com/channel/recently-updated*'),
                    Channels_Most_Subscribed=URL('http://www.redtube.com/channel/most-subscribed*'),
                    Channels_Most_Viewed=URL('http://www.redtube.com/channel/most-viewed*')
                    )

        view.add_start_button(picture_filename='model/site/resource/redtube.png',
                              menu_items=menu_items,
                              url=URL("http://www.redtube.com/", test_string='Redtube'))

    def get_shrink_name(self):
        return 'RT'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        # process thumbs
        for thumbnail in _iter(soup.find_all('div',{'class':'video_block_wrapper'})):
            try:
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['data-thumb_url'], base_url=url)
                label = thumbnail.img.attrs.get('alt', '')

                duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = collect_string(duration).strip('HD') if duration else ''

                hd_span = thumbnail.find('span', {'class': ['hd-video-icon','hd-video']})
                hd = '  HD' if hd_span else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'},
                                       {'text': hd, 'align': 'top left'}])
            except KeyError:
                pass

        # process channels
        for thumbnail in _iter(soup.find_all('li', {'class': 'channel-box'})):
            try:
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                label = thumbnail.img.attrs.get('alt', '')

                info = thumbnail.find('span', {'class': 'channels-list-info-span'})
                videos = collect_string(info) if info else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': videos, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'}])
            except KeyError:
                pass

        # process stars
        for thumbnail in _iter(soup.find_all('li', {'class': 'ps_info'})):
            try:
                href = URL(thumbnail.a.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['data-thumb_url'], base_url=url)
                label = thumbnail.img.attrs.get('alt', '')

                info = thumbnail.find('div', {'class': 'ps_info_count'})
                videos = collect_string(info) if info else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': videos, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'}])
            except KeyError:
                pass

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'id':'w_pagination_list'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'redtube-player'})
        if video:
            script = video.find('script', text=lambda x: 'video_player_setup' in str(x))
            if script:
                data = str(script.string).replace(' ', '').replace('\\', '')
                sources = quotes(data, 'mediaDefinition:[', ']').split('},{')
                for item in sources:
                    file = quotes(item, 'videoUrl":"', '"')
                    label = quotes(item, 'quality":"', '"')
                    if file:
                        self.add_video(label, URL(file, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        title=soup.find('div',{'class':'show_page_video_title'})
        if title:
            return collect_string(title.h1)
        else:
            return 'No title'

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        video_detail = soup.find('div', {'id': 'video_underplayer'})

        def process_tags(soup, cls, style=None):
            for item in _iter(soup.find_all('a', cls)):
                label = collect_string(item)
                href = item.attrs['href']
                self.add_tag(label, URL(href, base_url=url), style=style)

        # first add channel
        process_tags(video_detail,{'class':'video-infobox-link'},{'color':'blue'})

        # next star
        process_tags(video_detail, {'class': 'pornstar-name'}, {'color': 'red'})

        # next other
        process_tags(video_detail, {'class': None})

if __name__ == "__main__":
    pass

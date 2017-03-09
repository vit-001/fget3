__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class XhamsterSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('xhamster.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(HD_video=URL('https://ru.xhamster.com/channels/new-hd_videos-1.html*'),
                    Newest=URL('http://ru.xhamster.com/'),
                    Weekly_Top=URL('https://ru.xhamster.com/rankings/weekly-top-videos.html'),
                    Daily_Top=URL('https://ru.xhamster.com/rankings/daily-top-videos.html'),
                    Monthly_Top=URL('https://ru.xhamster.com/rankings/monthly-top-videos.html'),
                    Alltime_Top=URL('https://ru.xhamster.com/rankings/alltime-top-videos.html'),
                    )

        view.add_start_button(name='Xhmaster',
                              picture_filename='model/site/resource/xmaster.svg',
                              menu_items=menu_items,
                              url=URL("http://ru.xhamster.com/", test_string='xHamster'))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumb_container in _iter(soup.find_all('div',{'class':['box boxTL','box boxTR'], 'id':lambda x: x!='vPromo'})):
            for thumb in _iter(thumb_container.find_all('div',{'class':'video'})):
                # psp(thumb)
                href = URL(thumb.a.attrs['href'], base_url=url)
                description = thumb.a.img.attrs['alt']
                thumb_url = URL(thumb.img.attrs['src'], base_url=url)

                duration = thumb.find('b')
                dur_time = '' if duration is None else str(duration.string)

                quality = thumb.find('div', {'class': "hSpriteHD"})
                qual = '' if quality is None else 'HD'

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                labels=[{'text': dur_time, 'align': 'top right'},
                                        {'text': description, 'align': 'bottom center'},
                                        {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu=soup.find('div', {'id':'menuLeft'})
        if menu:
            hrefs=menu.find_all('a',{'href':lambda x: '/channels/' in x})
            for item in _iter(hrefs):
                label=''
                for s in item.stripped_strings:
                    label +=s
                href = item.attrs['href']
                self.add_tag(label.strip(), URL(href, base_url=url))

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'XHM '+ url.get().partition('xhamster.com/')[2].rpartition('.')[0]

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pager'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div', {'id': 'playerSwf'})
        if video is not None:
            script=video.find('script', text=lambda x: 'XPlayer' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\\/', '/')
                if 'sources:' in data:
                    sources=quotes(data,'sources:{','}').split('","')
                    for item in sources:
                        part=item.partition('":"')
                        file = part[2].strip('"')
                        label=part[0].strip('"')
                        self.add_video(label, URL(file, base_url=url))
                    self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info_box = soup.find('div', {'id': 'videoInfoBox'})
        for item in _iter(info_box.find_all('a')):
            # psp(item)
            label=''
            for s in item.stripped_strings:
                label +=s
            color = None
            href = item.attrs['href']
            if '/pornstars/' in href:
                color = 'magenta'
                # href += '/videos'
            if '/user/' in href:
                color = 'blue'
                href = href.replace('/user/','/user/video/')+'/new-1.html'

            self.add_tag(label.strip(), URL(href, base_url=url), style={'color':color})

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().rpartition('/')[2].rpartition('.')[0]


if __name__ == "__main__":
    pass
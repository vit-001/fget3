__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, pretty, collect_string, psp

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

        view.add_start_button(picture_filename='model/site/resource/xmaster.svg',
                              menu_items=menu_items,
                              url=URL("https://sv.xhamster.com/newest", test_string='xHamster'))

    def get_shrink_name(self):
        return 'XM'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumb_container in _iter(soup.find_all('div',{'class':'thumb-list'})):
            for thumb in _iter(thumb_container.find_all('div',{'class':'video-thumb'})):
                try:
                    # pretty(thumb)
                    href = URL(thumb.a.attrs['href'], base_url=url)
                    description = thumb.a.img.attrs['alt']
                    thumb_url = URL(thumb.img.attrs['src'], base_url=url)

                    duration = thumb.find('span', {'data-role-video-duration':True})
                    dur_time = '' if duration is None else str(duration.string)

                    quality = thumb.find('div', {'class': "hSpriteHD"})
                    qual = '' if quality is None else 'HD'

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                    labels=[{'text': dur_time, 'align': 'top right'},
                                            {'text': description, 'align': 'bottom center'},
                                            {'text': qual, 'align': 'top left', 'bold': True}])
                except AttributeError as e:
                    print(e.__repr__())

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
        return super().parse_thumb_title(soup, url).partition('.')[0]

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pager-container'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('script', {'id': 'initials-script'})
        if video:
            # pretty(video)
            script=str(video)
            if script:
                data = str(script).replace(' ', '').replace('\\/', '/')
                if '"sources":' in data:
                    # psp(data)
                    sources=quotes(data,'"sources":{','}').split('","')
                    # psp(sources)
                    for item in sources:
                        # psp(item)
                        part=item.partition('":"')
                        # psp(part)
                        file = part[2].strip('"')
                        label=part[0].strip('"')
                        self.add_video(label, URL(file, base_url=url))
                    self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info_box = soup.find('ul', {'class': 'categories-container'})
        if info_box:
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
                if '/users/' in href:
                    color = 'blue'
                    href = href+'/videos*'
                if '/channels/' in href:
                    color = 'green'
                    # href += '/videos'
                if '/creators/' in href:
                    color = 'blue'
                    # href += '/videos'


                self.add_tag(label.strip(), URL(href, base_url=url), style={'color':color})


if __name__ == "__main__":
    pass
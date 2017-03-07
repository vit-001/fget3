__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.base_site import BaseSiteParser


class V24videoSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('24videos.tv/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_Most_Recsent=URL('http://www.24videos.tv/latest-updates/'),
                    Videos_Most_Viewed=URL('http://www.24videos.tv/most-popular/'),
                    Videos_Top_Rated=URL('http://www.24videos.tv/top-rated/')
                    )

        view.add_start_button(name='24videos',
                              picture_filename='model/site/resource/24video.png',
                              menu_items=menu_items,
                              url=URL("http://www.24videos.tv/latest-updates/", test_string='24Videos.TV'))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'list-videos'})
        if container is not None:
            for thumbnail in _iter(container.find_all('div',{'class':'item'})):
                # psp(thumbnail.prettify())

                href = URL(thumbnail.a.attrs['href'], base_url=url)
                thumb_url = URL(thumbnail.img.attrs['data-original'], base_url=url)
                label=thumbnail.img.attrs.get('alt','')

                duration = thumbnail.find('div', {'class': 'duration'})
                dur_time = '' if duration is None else str(duration.contents[-1])

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                labels=[{'text':dur_time, 'align':'top right'},
                                        {'text':label, 'align':'bottom center'}])
#
    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination'})

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'V24 '+ url.get().partition('24videos.tv/')[2].strip('/')

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'class': 'player'})
        if content is not None:
            script =content.find('script', text=lambda x: 'flashvars' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '').replace('\n', '').replace('\t', '')
                flashvars = quotes(data,'flashvars={', '};').split(',')
                fv = dict()
                for flashvar in flashvars:
                    # print(flashvar)
                    split = flashvar.partition(':')
                    fv[split[0]] = split[2].strip("'\"")
                files = dict()
                for f in fv:
                    if fv[f].startswith('http://') and fv[f].endswith('.mp4/'):
                        file = fv[f]
                        label = fv.get(f + '_text', f)
                        files[label] = file

                print("=======================didn't work?")

                for key in sorted(files.keys(), reverse=True):
                    self.add_video(key, URL(files[key]))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().strip('/').rpartition('/')[2]


if __name__ == "__main__":
    pass

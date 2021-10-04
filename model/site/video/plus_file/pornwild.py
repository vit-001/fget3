__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornwildSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornwild.to/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(New=URL('https://pornwild.to/ru/latest-updates/'),
                    TopRated=URL('https://pornwild.to/ru/top-rated/'),
                    Popular=URL('https://pornwild.to/ru/most-popular/')
                    )

        view.add_start_button(picture_filename='model/site/resource/pornwind.svg',
                              menu_items=menu_items,
                              url=URL("https://pornwild.to/ru/latest-updates/"))

    def get_shrink_name(self):
        return 'PW'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        contents = soup.find('div', {'class':'list-videos'})
        if contents:
            # pretty(contents)

            for thumbnail in _iter(contents.find_all('div', {'class':'item'})):
                # try:
                #     pretty(thumbnail)

                    href = URL(thumbnail.a.attrs['href'], base_url=url)
                    # style= thumbnail.find('div',{'class':'img-src', 'style':True})
                    thumb_url = URL(thumbnail.img.attrs.get('data-original',thumbnail.img.attrs.get('data-webp','')))

                    title_tag = thumbnail.find('strong', {'class': 'title'})
                    label = '' if title_tag is None else collect_string(title_tag)

                    duration = thumbnail.find('div', {'class': 'duration'})
                    dur_time = '' if duration is None else str(duration.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'},
                                           ])
                # except AttributeError:
                #     pass

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu=soup.find('ul',{'class':'dropdown-menu'})
        if menu:
            for tag in menu.find_all('a', href=True):
                self.add_tag(str(tag.string).strip(),
                             URL(tag.attrs['href'], base_url=url),
                             style=dict(color='blue'))

        tags=soup.find('section', id='footer-tag')
        if tags:
            for tag in tags.find_all('a', href=True):
                self.add_tag(str(tag.string).strip(),
                             URL(tag.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = soup.find('div',{'class':'pagination-holder'})
        psp(url.get())
        if container:
            # baseurl=url.get().rstrip('/').rstrip('1234567890')+'/'
            baseurl = url.get().rstrip('/')
            if baseurl.rpartition('/')[2].isdecimal():
                baseurl=baseurl.rpartition('/')[0]

            for page in _iter(container.find_all('a', {'href': True})):
                # if page.string and str(page.string).strip().isdigit():
                    href=page.attrs['href']
                    if href == "#videos":
                        param=page.attrs['data-parameters']
                        pagenum=param.rpartition('from:')[2]
                        href=baseurl+'/'+pagenum+'/'

                    self.add_page(page.string.strip(), URL(href, base_url=url))
    #
    # def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
    #     pretty(soup.find('div',{'class':'pagination-holder'}))
    #     return soup.find('div',{'class':'pagination-holder'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'player-holder'})
        if container:
            # pretty(container)
            script=container.find('script', text=lambda x: 'kt_player' in str(x))
            if script:
                # psp(script)
                file_url=URL(quotes(script.string.replace(' ',''),'src="','"'),base_url=url)
                filedata=FLData(file_url,'')

                self._result_type = 'video'
                self.model.loader.start_load_file(filedata,self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        soup=BeautifulSoup(fldata.text, 'html.parser')
        script=soup.find('script', text=lambda x: 'flashvars' in str(x))

        flashvars=quotes(script.string.replace(' ',''),"flashvars={","};")

        vars=dict()
        for item in flashvars.split(','):
            split=item.partition(':')
            vars[split[0].strip()]=split[2].strip()

        if 'video_url' in vars:
            self.add_video(vars.get('video_url_text','???'), URL(vars['video_url'].strip("'")))

        if 'video_alt_url' in vars:
            self.add_video(vars.get('video_alt_url_text','???'), URL(vars['video_alt_url'].strip("'")))

        if 'video_alt_url2' in vars:
            self.add_video(vars.get('video_alt_url2_text','???'), URL(vars['video_alt_url2'].strip("'")))

        self.set_default_video(-1)
        self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class': 'info'})

        # pretty(container)

        for href in _iter(container.find_all('a',href=lambda x: '/sites/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style={'color': 'red'})

        for href in _iter(container.find_all('a',href=lambda x: '/models/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})

        for href in _iter(container.find_all('a',href=lambda x: '/categories/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))

        for href in _iter(container.find_all('a',href=lambda x: '/tags/' in str(x))):
            # psp(href)
            self.add_tag(collect_string(href), URL(href.attrs['href'], base_url=url))

if __name__ == "__main__":
    pass

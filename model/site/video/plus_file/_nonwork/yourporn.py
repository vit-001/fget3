__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser

class YPData(FLData):
    def __init__(self, url: URL, part: str):
        super().__init__(url, '')
        self.part=part

class YourpornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('yourporn.sexy/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Latest=URL('https://yourporn.sexy/blog/all/0.html?sm=latest*'),
                    Views=URL('https://yourporn.sexy/blog/all/0.html?sm=views*'),
                    Rating=URL('https://yourporn.sexy/blog/all/0.html?sm=rating*'),
                    Orgazmic=URL('https://yourporn.sexy/blog/all/0.html?sm=orgasmic*'),
                    )

        view.add_start_button(picture_filename='model/site/resource/youporn.png',
                              menu_items=menu_items,
                              url=URL("https://yourporn.sexy/blog/all/0.html*", test_string='YourPorn'))

    def get_shrink_name(self):
        return 'YP'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for post in _iter(soup.find_all('div', {'class':'post_el'})):
            try:
                author=post.find('a',{'class':'span_author_name'})
                author_str=str(author.span.string).strip()

                combo=post.find('div',{'class':'combo_post_wrap'})
                if combo:
                    href = URL(combo.a.attrs['href'], base_url=url)
                    description = combo.a.attrs['title']
                    thumb_url = URL(combo.img.attrs['src'], base_url=url)

                    dur_time = 'Multi'

                else:
                    vid_container = post.find('div', {'class': 'vid_container'})

                    href = URL(vid_container.a.attrs['href'], base_url=url)

                    description = vid_container.a.attrs['title']
                    thumb_url = URL(vid_container.img.attrs['src'], base_url=url)

                    duration = post.find('span', {'class': "duration_small"})
                    dur_time = '' if duration is None else str(duration.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': author_str, 'align': 'top left'},
                                       {'text': description, 'align': 'bottom center'}])
            except AttributeError:
                pass

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        pagination = soup.find('div', {'id': 'center_control'})
        if pagination is not None:
            for page in _iter(pagination.find_all('a')):
                href=page.attrs['href']
                num= href.rpartition('/')[2].partition('.')[0]
                self.add_page(num, URL(href, base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        videos_container = soup.find('div', {'id': 'videos_container'})
        video_container = soup.find('div', {'itemprop': 'video'})

        if videos_container:
            usss=soup.find('script',text=lambda x: 'usss' in str(x))
            uid=quotes(usss.string.replace(' ',''),'usss[0]="','"')

            xhr_list=list()
            part=1
            for data_div in _iter(videos_container.find_all('div', {'class':'pl_vid_el'})):
                data = {'uid': uid, 'source': data_div.attrs['data-source'], 'hash': data_div.attrs['data-hash'],
                            'x': data_div.attrs['data-x'],
                            'oid': data_div.attrs['data-oid'], 'pid': data_div.attrs['data-pid']}

                xhr=URL('/php/get_vlink.php',base_url=url,method='POST',post_data=data)
                xhr_list.append(YPData(xhr,' - Part {0}'.format(part)))
                part += 1

            loader=self.model.loader
            load_process=loader.get_new_load_process(self.add_part)

            self._result_type = 'video'
            load_process.load_list(xhr_list)

        elif video_container:
            video=video_container.find('video')
            if video:
                self.add_video('default', URL(video.attrs['src'], base_url=url))

    def add_part(self, ypdata:YPData):
        self.add_video('default', URL(ypdata.text, base_url=self.url))

        save_title=self.title
        self.title=save_title + ypdata.part

        self.generate_video_view()

        self.title=save_title
        self.start_options['current_full_view']=None
        self.video_data = []

    def parse_video_title(self, soup:BeautifulSoup, url:URL)->str:
        title=''
        post_text=soup.find('div', {'class':'post_text'})
        for txt in post_text.stripped_strings:
            if not txt.startswith('#'):
                title+=' '+txt
        return title

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):

        author=soup.find('div',{'class':'post_author_name'})
        if author:
            self.add_tag(str(author.span.string), URL(author.a.attrs['href'], base_url=url), style={'color': 'blue'})

        for tags_container in _iter(soup.find_all('div',{'class':'popular_block_header_rl'})):
            for tag in _iter(tags_container.find_all('a')):
                self.add_tag(str(tag.b.string).strip(),URL(tag.attrs['href'],base_url=url))

if __name__ == "__main__":
    pass

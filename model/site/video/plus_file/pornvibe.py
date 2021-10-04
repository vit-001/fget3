# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string, pretty, collect_string_to_array

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornvibeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornvibe.org/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        # menu_items=dict(Channels=URL('http://www.pornbozz.com/channels/'),
        #             Galleries_Recent=URL('http://www.pornbozz.com/photos/'),
        #             Galleries_Most_Viewed=URL('http://www.pornbozz.com/photos/most-viewed/'),
        #             Galleries_Top_Rated=URL('http://www.pornbozz.com/photos/top-rated/'),
        #             Videos_Recent=URL('http://www.pornbozz.com/videos/'),
        #             Videos_Most_Viewed=URL('http://www.pornbozz.com/most-viewed/'),
        #             Videos_Top_Rated=URL('http://www.pornbozz.com/top-rated/'),
        #             Videos_Longest=URL('http://www.pornbozz.com/longest/'))

        view.add_start_button(picture_filename='model/site/resource/pornvibe.png',
                              url=URL("https://pornvibe.org/all-videos/"))

    def get_shrink_name(self):
        return 'PBZ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div', {'class':'list-group'})
        if container:
            # pretty(container)
            for thumbnail in _iter(soup.find_all('div', {'class': 'post'})):
                try:
                    # pretty(thumbnail)
                    picture=thumbnail.find('div',{'class':'post-thumb'})
                    text=thumbnail.find('div',{'class':'post-des'})
                    # pretty(picture)
                    # pretty(text)

                    xref=text.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)
                    description = collect_string(xref)

                    img=picture.find('img', src=True)
                    thumb_url = URL(img.attrs['src'], base_url=url)

                    duration = picture.find('div', {'class': "thumb-stats pull-right"})
                    dur_time = '' if duration is None else collect_string(duration)
                    #
                    # quality = thumbnail.find('span', {'class': "quality-icon"})
                    # qual = '' if quality is None else str(quality.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                               labels=[{'text': dur_time, 'align': 'top right'},
                                                       {'text': description, 'align': 'bottom center'}])
                except AttributeError as e:
                    print(e.__repr__())

    def parse_others(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'main-cat'})
        if container:
            pretty(container)
            for thumbnail in _iter(soup.find_all('div', {'class': 'item-cat'})):
                # pretty(thumbnail)
                picture=thumbnail.find('img',alt=True, src=True)
                if picture:
                    # text=thumbnail.find('div',{'class':'post-des'})
                    # # pretty(picture)
                    # # pretty(text)

                    xref=thumbnail.find('a', href=True)
                    href = URL(xref.attrs['href'], base_url=url)
                    description = picture.attrs['alt']
                    thumb_url = URL(picture.attrs['src'], base_url=url)

                    # duration = picture.find('div', {'class': "thumb-stats pull-right"})
                    # dur_time = '' if duration is None else collect_string(duration)
                    #
                    # quality = thumbnail.find('span', {'class': "quality-icon"})
                    # qual = '' if quality is None else str(quality.string)

                    count=collect_string_to_array(thumbnail)[-1]

                    # psp(thumb_url,href,description,count)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                               labels=[{'text': count, 'align': 'top right'},
                                                       {'text': description, 'align': 'bottom center'}])

        # for thumbnail in _iter(soup.find_all('div', {'class': 'item-inner-col'})):
        #     href = URL(thumbnail.a.attrs['href'], base_url=url)
        #     thumb_url = URL(thumbnail.img.attrs['src'])
        #     description = thumbnail.img.attrs['alt']
        #
        #     self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
        #                    labels=[{'text': description, 'align': 'bottom center'}])


    # def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
    #     container=soup.find('ul',{'class':'simple-list--channels'})
    #     if container:
    #         for channel in _iter(container.find_all('a',href=True, title=True)):
    #             self.add_tag(str(channel.attrs['title']),URL(channel.attrs['href']))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('meta',src=True, content=lambda x: 'fvplayer' in str(x))
        if video:
            # pretty(video)
            self.add_video('default', URL(video.attrs['src'], base_url=url))
        else:
            container = soup.find('div', {'class': 'flex-video'})
            if container:
                # pretty(container)
                frame=container.find('iframe', src=True)
                if frame:
                    # pretty(frame)
                    file_url=URL(frame.attrs['src'],base_url=url)
                    filedata=FLData(file_url,'')

                    self._result_type = 'video'
                    self.model.loader.start_load_file(filedata,self.continue_parse_video)


    # def parse_video(self, soup: BeautifulSoup, url: URL):
    #     container=soup.find('div',{'class':'player-holder'})
    #     if container:
    #         # pretty(container)
    #         script=container.find('script', text=lambda x: 'kt_player' in str(x))
    #         if script:
    #             # psp(script)

    def continue_parse_video(self, fldata:FLData):
        soup=BeautifulSoup(fldata.text, 'html.parser')
        # pretty(soup)
        video = soup.find('video', {'class':'video-js'})
        if video:
            # pretty(video)
            source=video.find('source', src=True)
            if source:
                self.add_video('default', URL(source.attrs['src']))
                self.generate_video_view()

        #
        # script=soup.find('script', text=lambda x: 'flashvars' in str(x))
        #
        # flashvars=quotes(script.string.replace(' ',''),"flashvars={","};")
        #
        # vars=dict()
        # for item in flashvars.split(','):
        #     split=item.partition(':')
        #     vars[split[0].strip()]=split[2].strip()
        #
        # if 'video_url' in vars:
        #     self.add_video(vars.get('video_url_text','???'), URL(vars['video_url'].strip("'")))
        #
        # if 'video_alt_url' in vars:
        #     self.add_video(vars.get('video_alt_url_text','???'), URL(vars['video_alt_url'].strip("'")))
        #
        # if 'video_alt_url2' in vars:
        #     self.add_video(vars.get('video_alt_url2_text','???'), URL(vars['video_alt_url2'].strip("'")))
        #
        # self.set_default_video(-1)


    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        cat_container=soup.find('div',{'class':'categories'})
        if cat_container:
            for tag in _iter(cat_container.find_all('a',href=True)):
                self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))

        tag_container=soup.find('div',{'class':'tags'})
        if tag_container:
            for tag in _iter(tag_container.find_all('a',href=True)):
                self.add_tag(collect_string(tag), URL(tag.attrs['href'], base_url=url))

        # xref=user_container.find('a',href=True,title=True)
        # if user_container:
        #     username=str(xref.attrs['title'])
        #     href=str(xref.attrs['href'])
        #     user_number=href.rstrip('/').rpartition('-')[2]
        #
        #     self.add_tag(username + ' videos',
        #                  URL('http://www.pornbozz.com/uploads-by-user/{0}/'.format(user_number)),
        #                  style={'color': 'blue'})
        #
        #     self.add_tag(username +  ' photos',
        #                  URL('http://www.pornbozz.com/uploads-by-user/{0}/?photos=1'.format(user_number)),
        #                  style={'color': 'blue'})
        #


    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        gallery=soup.find('div',{'class':'gallery-block'})
        if gallery:
            for image in _iter(gallery.find_all('img',src=True)):
                image_url=URL(str(image.attrs['src']).replace('/thumbs/','/'))
                filename = image_url.get_path() + image_url.get().rpartition('/')[2]
                self.add_picture(filename, image_url)

    def parse_pictures_tags(self, soup: BeautifulSoup, url: URL):
        self.parse_video_tags(soup,url)

if __name__ == "__main__":
    pass

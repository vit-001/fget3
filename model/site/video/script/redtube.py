__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp

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
        thumbnail_containers = soup.find_all('ul', {'class': ['thumb-list','video-listing']})
        channel_containers = soup.find_all('ul', {'class': ['channels-list']})
        stars_containers = soup.find_all('ul', {'class': ['pornStarsThumbs']})

        if thumbnail_containers and len(thumbnail_containers) > 0:
            # parce thumbnail page
            for thumbnail_container in thumbnail_containers:
                for thumbnail in _iter(thumbnail_container.find_all('li')):
                    try:
                        # psp(thumbnail.prettify())
                        href = URL(thumbnail.a.attrs['href'], base_url=url)
                        thumb_url = URL(thumbnail.img.attrs['data-src'], base_url=url)
                        label = thumbnail.img.attrs.get('alt', '')

                        duration = thumbnail.find('span', {'class': ['widget-video-duration','video-duration']})
                        dur_time = '' if duration is None else str(duration.string).strip()

                        hd_span = thumbnail.find('span', {'class': ['hd-video-icon','hd-video']})
                        hd = '' if hd_span is None else '  HD'

                        self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                       labels=[{'text': dur_time, 'align': 'top right'},
                                               {'text': label, 'align': 'bottom center'},
                                               {'text': hd, 'align': 'top left'}])
                    except KeyError:
                        pass

        elif channel_containers is not None and len(channel_containers) > 0:
            # parce channels page
            for channel_container in channel_containers:
                for channel in _iter(channel_container.find_all('li')):
                    href = URL(channel.a.attrs['href'], base_url=url)
                    logo = channel.find('span', {'class': 'channel-logo'})
                    img = logo.find('img')
                    if img is None:
                        img = channel.find('img')
                    thumb_url = URL(img.attrs.get('data-src', img.attrs['src']), base_url=url)
                    label = channel.img.attrs.get('alt', '')

                    num_videos_span = channel.find('span', text=lambda x: 'videos' in str(x))
                    num_videos = '' if num_videos_span is None else str(num_videos_span.string).strip()

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text': num_videos, 'align': 'top right'},
                                           {'text': label, 'align': 'bottom center'}])

        elif stars_containers is not None and len(stars_containers) > 0:

            # unlock http://www.pornhub.com/
            self.model.loader.start_load_file(FLData(URL('http://pornhub.com/',test_string='Tube'), ''),
                                              on_result=lambda x: self.continue_with_stars(FLData(url,''), soup))
            self.waiting_data=True
            # adding tags to stars page
            tags_containers = _iter(soup.find_all('ul', {'class': ['abc-categories']}))
            for tags_container in tags_containers:
                for tag in _iter(tags_container.find_all('a')):
                    # print(tag)
                    self.add_tag(str(tag.string), URL(tag.attrs['href'], base_url=url))

    def continue_with_stars(self, filedata:FLData, soup:BeautifulSoup):
        # parce stars page
        self.waiting_data=False
        for stars_container in soup.find_all('ul', {'class': ['pornStarsThumbs']}):
            for star in _iter(stars_container.find_all('li')):
                href = URL(star.a.attrs['href'], base_url=filedata.url)
                img = star.find('img')
                thumb_url = URL(img.attrs['src'], base_url=filedata.url)
                label = img.attrs.get('alt', '')

                num_videos_span = star.find('span', text=lambda x: 'Videos' in str(x))
                num_videos = '' if num_videos_span is None else str(num_videos_span.string)

                self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                               labels=[{'text': num_videos, 'align': 'top right'},
                                       {'text': label, 'align': 'bottom center'}])
        self.generate_thumb_view()

    # def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
    #     return 'RT '+ url.get().partition('redtube.com/')[2]

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_containers = _iter(soup.find_all('ul', {'class': ['categories-listing', 'categories-popular-listing']}))
        for tags_container in tags_containers:
            for tag in _iter(tags_container.find_all('a')):
                self.add_tag(str(tag.attrs['title']), URL(tag.attrs['href'], base_url=url))

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        pagination = soup.find('div', {'class': 'pages'})
        if pagination:
            for page in _iter(pagination.find_all('a')):
                num = '' if page.string is None else str(page.string)
                if num.isdigit():
                    self.add_page(num, URL(page.attrs['href'], base_url=url))
            return

        pagination_v2=soup.find('ul',{'id':'w_pagination_list'})
        if pagination_v2:
            # psp(pagination_v2.prettify())
            for page in _iter(pagination_v2.find_all('a')):
                # psp(page)
                num = page.span.string
                if num.isdigit():
                    self.add_page(num, URL(page.attrs['href'], base_url=url))


    def parse_video(self, soup: BeautifulSoup, url: URL):
        psp(soup)
        video = soup.find('div', {'class': 'watch'})
        if video:
            script = video.find('script', text=lambda x: 'redtube_flv_player' in str(x))
            if script:
                data = str(script.string).replace(' ', '').replace('\\', '')
                psp(data)
                sources = quotes(data, 'mediaDefinition:[', ']').split('},{')
                for item in sources:
                    file = quotes(item, 'videoUrl":"', '"')
                    label = quotes(item, 'quality":"', '"')
                    if file:
                        self.add_video(label, URL(file, base_url=url))

                        # self.sort_video()
                        # self.set_default_video(-1)

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        title=soup.find('h1',{'class':'videoTitle'})
        if title:
            return title.string
        else:
            return 'No title'

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        video_detail = soup.find('div', {'class': 'video-details'})
        # first add user reference
        user_container = video_detail.find('td', {'class': 'withbadge'})
        if user_container:
            user = user_container.find('a')
            if user:
                href = user.attrs['href']
                username = user.string
                self.add_tag(username, URL(href, base_url=url), style={'color':'blue'})
        # stars in video adding
        stars_container = video_detail.find('ul', {'class': 'pornstars-in-video'})
        if stars_container:
            stars = _iter(stars_container.find_all('li', {'class': None}, recursive=False))
            for star in stars:
                href = star.find('a')
                if href:
                    info = list(star.find('span', {'class': 'pornstar-info'}).stripped_strings)
                    name = info[0] + ' ' + info[1]
                    url = URL(href.attrs['href'], base_url=url)
                    self.add_tag(name, url, style={'color':'magenta'})
        # other tags
        for links_container in _iter(video_detail.find_all('td', {'class': 'links'})):
            for href in _iter(links_container.find_all('a', {'href': lambda x: 'javascript' not in x})):
                if href.string:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))
#

if __name__ == "__main__":
    pass

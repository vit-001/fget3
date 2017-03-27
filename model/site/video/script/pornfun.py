# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes , psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornfunSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornfun.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_New=URL('http://pornfun.com/latest-updates/'),
                    Videos_Most_Popular_Today=URL('http://pornfun.com/most-popular/today/'),
                    Videos_Most_Popular_Week=URL('http://pornfun.com/most-popular/week/'),
                    Videos_Most_Popular_Month=URL('http://pornfun.com/most-popular/month/'),
                    Videos_Most_Popular_All_Time=URL('http://pornfun.com/most-popular/'),
                    Videos_Top_Rated_Today=URL('http://pornfun.com/top-rated/today/'),
                    Videos_Top_Rated_Week=URL('http://pornfun.com/top-rated/week/'),
                    Videos_Top_Rated_Month=URL('http://pornfun.comtop-rated/month/'),
                    Videos_Top_Rated_All_Time=URL('http://pornfun.com/top-rated/'),
                    Videos_Longest=URL('http://pornfun.com/longest/'),
                    Video_Categories=URL('http://pornfun.com/categories/'),
                    Photo_Categories=URL('http://pornfun.com/albums/categories/'),
                    Photo_New=URL('http://pornfun.com/albums/'),
                    Photo_Popular=URL('http://pornfun.com/albums/most-popular/'),
                    Photo_Top_Rated=URL('http://pornfun.com/albums/top-rated/')
                    )

        view.add_start_button(picture_filename='model/site/resource/pornfun.png',
                              menu_items=menu_items,
                              url=URL("http://pornfun.com/latest-updates/"))

    def get_shrink_name(self):
        return 'PF'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for content in _iter(soup.find_all('div', {'class':'content'})):
            for thumbnail in _iter(content.find_all('li', {'class': 'thumb'})):
                # psp(thumbnail.prettify())
                href = URL(thumbnail.a.attrs['href'], base_url=url)

                name = thumbnail.find('span', {'class': 'thumb-title'})
                description = '' if name is None else str(name.string)
                thumb_url = URL(thumbnail.img.attrs['data-original'], base_url=url)

                duration = thumbnail.find('span', {'class': 'duration'})
                dur_time = '' if duration is None else str(duration.string)

                if dur_time != 'Link':
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        list_cat=soup.find('div', {'class', 'list-categories'})
        for href in _iter(list_cat.find_all('a')):
            self.add_tag(str(href.attrs['title']), URL(href.attrs['href'], base_url=url))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'class': 'player-holder'})
        if content is not None:
            script = content.find('script', text=lambda x: 'video_url:' in str(x))
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, "video_url:'", "'").replace('https','http')#.rstrip('/')
                self.add_video('DEFAULT', URL(file+'*', base_url=url))

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        user_info= soup.find('div', {'class':'user-info'})
        if user_info:
            self.add_tag(str(user_info.a.attrs['title']), URL(user_info.a.attrs['href']+'public_videos/', base_url=url),
                         style={'color': 'blue'})

        specification=soup.find('div', {'class':'specification'})
        if specification:
            for href in _iter(specification.find_all('a')):
                self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))



#
#     def parse_index_file(self, fname, base_url=URL()):
#         parser = SiteParser()
#
#         # def star_get_url(txt=''):
#         #     return txt.partition('(')[2].partition(')')[0]
#
#         startpage_rule = ParserRule()
#         startpage_rule.add_activate_rule_level([('ul', 'class', 'thumbs-items'),
#                                                 ('ul', 'class', 'thumbs-albums'),
#                                                 ('ul', 'class', 'thumbs-categories')])
#         startpage_rule.add_process_rule_level('a', {'href'})
#         startpage_rule.add_process_rule_level('img', {'data-original', 'alt'})
#         startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         # startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x,base_url))
#         parser.add_rule(startpage_rule)
#
#         startpage_pages_rule = ParserRule()
#         startpage_pages_rule.add_activate_rule_level([('div', 'class', 'pagination')])
#         # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
#         startpage_pages_rule.add_process_rule_level('a', {'href'})
#         startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         parser.add_rule(startpage_pages_rule)
#
#         startpage_hrefs_rule = ParserRule()
#         startpage_hrefs_rule.add_activate_rule_level([('div', 'class', 'list-categories')])
#         # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
#         startpage_hrefs_rule.add_process_rule_level('a', {'href', 'title'})
#         # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/videos/' in x)
#         startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         parser.add_rule(startpage_hrefs_rule)
#         #
#         video_rule = ParserRule()
#         video_rule.add_activate_rule_level([('div', 'class', 'player-holder')])
#         video_rule.add_process_rule_level('script', {})
#         video_rule.set_attribute_filter_function('data', lambda text: 'video_url:' in text)
#         parser.add_rule(video_rule)
#         #
#         gallery_href_rule = ParserRule()
#         gallery_href_rule.add_activate_rule_level([('div', 'class', 'specification')])
#         gallery_href_rule.add_process_rule_level('a', {'href'})
#         gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         parser.add_rule(gallery_href_rule)
#
#         gallery_user_rule = ParserRule(collect_data=True)
#         gallery_user_rule.add_activate_rule_level([('div', 'class', 'user-info')])
#         gallery_user_rule.add_process_rule_level('a', {'href', 'title'})
#         # gallery_user_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x+'/videos',base_url))
#         # gallery_user_rule.set_attribute_filter_function('href',lambda x:'/members/' in x)
#         parser.add_rule(gallery_user_rule)
#
#         photo_rule = ParserRule()
#         photo_rule.add_activate_rule_level([('div', 'class', 'ad-thumbs')])
#         photo_rule.add_process_rule_level('a', {'data-image'})
#         # photo_rule.set_attribute_filter_function('href', lambda text: '/photos/' in text)
#         photo_rule.set_attribute_modifier_function('data-image', lambda x: self.get_href(x, base_url))
#         parser.add_rule(photo_rule)
#
#         self.proceed_parcing(parser, fname)
#
#         result = ParseResult()
#
#         def add_href_and_user_to_result():
#             if gallery_user_rule.is_result(['href']):
#                 for item in gallery_user_rule.get_result(['href']):
#                     # print(item)
#                     username = item['title']
#                     # print(username)
#                     if username != '':
#                         result.add_control(
#                             ControlInfo('"' + username + ' videos"', URL(item['href'] + 'public_videos/')))
#                         result.add_control(ControlInfo('"' + username + ' photos"', URL(item['href'] + 'albums/')))
#
#             for f in gallery_href_rule.get_result(['data', 'href']):
#                 result.add_control(ControlInfo(f['data'], URL(f['href'])))
#
#         if video_rule.is_result():  # len(video_rule.get_result()) > 0:
#
#             # for item in video_rule.get_result():
#             #     print('=============================')
#             #     print(item['data'])
#
#             script = video_rule.get_result()[0]['data'].replace(' ', '')
#             # print(script)
#
#             url = script.partition("video_url:'")[2].partition("'")[0].rstrip('/')
#             print(url)
#
#             video = MediaData(URL(url))
#             result.set_type('video')
#             result.set_video(video)
#
#             add_href_and_user_to_result()
#             return result
#
#         if photo_rule.is_result():
#             result.set_type('pictures')
#             base_dir = base_url.get_path(base=Setting.base_dir) + base_url.get().rpartition('/')[2] + '/'
#             result.set_gallery_path(base_dir)
#             # print(base_dir)
#
#             for item in photo_rule.get_result():
#                 name = item['data-image'].rpartition('/')[2].strip('*')
#                 picture = FullPictureInfo(abs_href=URL(item['data-image']), rel_name=name)
#                 picture.set_base(base_dir)
#                 result.add_full(picture)
#
#             add_href_and_user_to_result()
#
#             return result
#
#         if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
#             result.set_type('hrefs')
#
#             for item in startpage_rule.get_result(['href', 'data-original']):
#                 # print(item)
#                 href = item['href']
#                 label = href.split('/')[-2].upper().replace('-', ' ')
#                 # print(href,label)
#
#                 result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(href), popup=label))
#
#             for item in startpage_pages_rule.get_result(['href', 'data']):
#                 result.add_page(ControlInfo(item['data'], URL(item['href'])))
#
#             if len(startpage_hrefs_rule.get_result(['href'])) > 0:
#                 for item in startpage_hrefs_rule.get_result(['href', 'title']):
#                     result.add_control(ControlInfo(item.get('title', item.get('data', '')), URL(item['href'])))
#
#         return result
#

if __name__ == "__main__":
    pass

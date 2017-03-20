# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup
import json

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PornbrazeSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornbraze.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Videos_Most_Recsent=URL('http://pornbraze.com/recent/'),
                        Videos_HD=URL('http://pornbraze.com/hd-porn/'),
                        Videos_Longest=URL('http://pornbraze.com/longest/'),
                        Videos_Downloaded=URL('http://pornbraze.com/downloaded/'),
                        Videos_Most_Popular=URL('http://pornbraze.com/popular/'),  #
                        DVDs=URL('http://pornbraze.com/dvd/'),
                        Channels=URL('http://pornbraze.com/channels/')
                        )

        view.add_start_button(picture_filename='model/site/resource/pornbaze.png',
                              menu_items=menu_items,
                              url=URL("http://pornbraze.com/recent/"))

    def get_shrink_name(self):
        return 'PBZ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'video'})):
            href = URL(thumbnail.a.attrs['href'], base_url=url)
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
            label=thumbnail.img.attrs.get('alt','')

            duration = thumbnail.find('span', {'class': 'video-overlay'})
            dur_time = '' if duration is None else str(duration.string)

            hd_span = thumbnail.find('span', {'class': 'hdmovie-icon'})
            hd = 'HD' if hd_span else ''

            self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                           labels=[{'text':dur_time, 'align':'top right'},
                                   {'text':label, 'align':'bottom center'},
                                   {'text': hd, 'align': 'top left'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'class':'pagination'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu=soup.find('div',{'class':'menu-box'})

        # categories=menu.find('div',{'id':'categories-subnav-box'})
        # for tag in _iter(categories.find_all('a')):
        #     self.add_tag(collect_string(tag),URL(tag.attrs['href']))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        player_container = soup.find('div', {'id':'player'})
        if player_container:
            script=player_container.find('script', text=lambda text: 'jwplayer' in str(text))
            if script:
                text=script.string
                if 'sources:[' in text:
                    sources = quotes(text, 'sources:[', ']')
                    j = json.loads('['+sources+']')
                    for j_data in j:
                        if j_data['file'] is not '':
                            self.add_video(j_data['label'],URL(j_data['file']+'*'))
                            self.set_default_video(-1)
                elif 'sources:' in text:
                    container = soup.find('div', {'class': 'content-video'})
                    if container:
                        script = container.find('script',{'src':lambda x: '/player/' in str(x)})
                        if script:
                            script_url=URL(script.attrs['src'],base_url=url)
                            filedata = FLData(script_url, '')

                            self._result_type = 'video'
                            self.model.loader.start_load_file(filedata, self.continue_parse_video)

    def continue_parse_video(self, fldata:FLData):
        bitrates=quotes(fldata.text,"'bitrates':[{","}]").split('},{')
        for item in bitrates:
            file=quotes(item,"'file':'","'")
            label=quotes(item,'label:"','"')
            self.add_video(label,URL(file))
        self.set_default_video(-1)
        self.generate_video_view()

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # info_box=soup.find('div',{'class':'content-container'})
        for info_box in _iter(soup.find_all('div',{'class':'content-container'})):
            # psp(info_box.prettify())
            for href in _iter(info_box.find_all('a', href=True)):
                psp(href.prettify())
                label=collect_string(href)
                href_url=URL(href.attrs['href'],base_url=url)
                print(label,href_url)

                color=None

                if href_url.contain('/users/'):
                    color='blue'
                    href_url=URL(href_url.get()+'/videos/public/')

                if href_url.contain('/pornstar/'):
                    color='red'

                self.add_tag(label,href_url,style=dict(color=color))


#
# class PBZvideoSite(BaseSite):
#     def start_button_name(self):
#         return "PBZvid"
#
#     def get_start_button_menu_text_url_dict(self):
#         return dict(Videos_Most_Recsent=URL('http://pornbraze.com/recent/'),
#                     Videos_HD=URL('http://pornbraze.com/hd-porn/'),
#                     Videos_Longest=URL('http://pornbraze.com/longest/'),
#                     Videos_Downloaded=URL('http://pornbraze.com/downloaded/'),
#                     Videos_Most_Popular=URL('http://pornbraze.com/popular/'),  #
#                     DVDs=URL('http://pornbraze.com/dvd/'),
#                     Channels=URL('http://pornbraze.com/channels/')
#                     )
#
#     def startpage(self):
#         return URL("http://pornbraze.com/recent/")
#
#     def can_accept_index_file(self, base_url=URL()):
#         return base_url.contain('pornbraze.com/')
#
#     def parse_index_file(self, fname, base_url=URL()):
#         parser = SiteParser()
#
#         startpage_rule = ParserRule()
#         startpage_rule.add_activate_rule_level([('div', 'class', 'video')])
#         startpage_rule.add_process_rule_level('a', {'href', 'title'})
#         startpage_rule.add_process_rule_level('img', {'src', 'alt'})
#         startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
#         parser.add_rule(startpage_rule)
#
#         channels_rule = ParserRule()
#         channels_rule.add_activate_rule_level([('ul', 'class', 'channels')])
#         channels_rule.add_process_rule_level('a', {'href', 'title'})
#         channels_rule.add_process_rule_level('div', {})
#         channels_rule.add_process_rule_level('img', {'src', 'alt'})
#         channels_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url).replace('*', '/'))
#         channels_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
#         parser.add_rule(channels_rule)
#
#         startpage_pages_rule = ParserRule()
#         startpage_pages_rule.add_activate_rule_level([('ul', 'class', 'pagination pagination-lg')])
#         # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
#         startpage_pages_rule.add_process_rule_level('a', {'href'})
#         startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         parser.add_rule(startpage_pages_rule)
#
#         startpage_hrefs_rule = ParserRule()
#         startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'nav nav-stacked navigation')])
#         # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
#         startpage_hrefs_rule.add_process_rule_level('a', {'href'})
#         # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/videos/' in x)
#         startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         parser.add_rule(startpage_hrefs_rule)
#         #
#         video_rule = ParserRule()
#         video_rule.add_activate_rule_level([('div', 'id', 'player')])
#         video_rule.add_process_rule_level('script', {})
#         video_rule.set_attribute_filter_function('data', lambda text: 'jwplayer' in text)
#         # video_rule.set_attribute_modifier_function('src',lambda x:self.get_href(x,base_url))
#         parser.add_rule(video_rule)
#
#         video2_rule = ParserRule()
#         video2_rule.add_activate_rule_level([('div', 'id', 'video')])
#         video2_rule.add_process_rule_level('script', {'src'})
#         video2_rule.set_attribute_filter_function('src', lambda text: 'pornbraze.com/' in text)
#         video2_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
#         parser.add_rule(video2_rule)
#
#         #
#         gallery_href_rule = ParserRule()
#         gallery_href_rule.add_activate_rule_level([('div', 'class', 'col-xs-12 col-sm-12 col-md-12')])
#         gallery_href_rule.add_process_rule_level('a', {'href'})
#         gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
#         parser.add_rule(gallery_href_rule)
#
#         self.proceed_parcing(parser, fname)
#
#         result = ParseResult()
#
#         if video_rule.is_result():  # len(video_rule.get_result()) > 0:
#
#             urls = list()
#             for item in video_rule.get_result():
#                 # print(item['data'])
#                 script = item['data'].replace(' ', '')
#                 if 'sources:[{' in script:
#                     txt = '[{' + self.quotes(item['data'].replace(' ', ''), 'sources:[{', '}]') + '}]'
#                     j = json.loads(txt)
#                     for j_data in j:
#                         # print(j_data)
#                         if j_data['file'] is not '':
#                             data = dict(text=j_data['label'], url=URL(j_data['file'] + '*'))
#                             urls.append(data)
#                 elif 'sources:' in script:
#                     if video2_rule.is_result(['src']):
#                         # print(video2_rule.get_result())
#                         php_url = URL(video2_rule.get_result(['src'])[0]['src'])
#                         # print(php_url)
#                         res = load(php_url)
#                         # print(res.text)
#                         bitrates = self.quotes(res.text, "'bitrates':[{", "}]").split('},{')
#                         # print(bitrates)
#                         for line in bitrates:
#                             print(line)
#                             video_url = self.quotes(line, "'file':'", "'")
#                             label = self.quotes(line, 'label:"', '"')
#                             data = dict(text=label, url=URL(video_url + '*'))
#                             urls.append(data)
#
#             if len(urls) == 1:
#                 video = MediaData(urls[0]['url'])
#             elif len(urls) > 1:
#                 video = MediaData(urls[0]['url'])
#                 for item in urls:
#                     video.add_alternate(item)
#             else:
#                 return result
#
#             result.set_type('video')
#             result.set_video(video)
#
#             for f in gallery_href_rule.get_result(['data', 'href']):
#                 # print(f)
#                 href = f['href'].replace('*', '/')
#                 label = f['data']
#                 if '/users/' in href:
#                     href = href + '/videos/public/'
#                     label = '"' + label + '"'
#
#                 result.add_control(ControlInfo(label, URL(href)))
#
#             return result
#
#         if startpage_rule.is_result() or channels_rule.is_result():
#             result.set_type('hrefs')
#
#             for item in startpage_rule.get_result(['href']):
#                 result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),
#                                            popup=item.get('alt', item.get('title', ''))))
#
#             for item in channels_rule.get_result(['href']):
#                 result.add_thumb(ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),
#                                            popup=item.get('alt', item.get('title', ''))))
#
#             for item in startpage_pages_rule.get_result(['href', 'data']):
#                 result.add_page(ControlInfo(item['data'], URL(item['href'])))
#
#             for item in startpage_hrefs_rule.get_result():
#                 label = item['href'].strip('*/').rpartition('/')[2]
#                 result.add_control(ControlInfo(label, URL(item['href'])))
#
#         return result
#

if __name__ == "__main__":
    pass

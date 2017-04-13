# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class ThumbzillaSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('thumbzilla.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Hottest=URL('https://www.thumbzilla.com/'),
                    Newest=URL('https://www.thumbzilla.com/newest*'),
                    Top=URL('https://www.thumbzilla.com/top*'),
                    Trending=URL('https://www.thumbzilla.com/trending*'),
                    Popular=URL('https://www.thumbzilla.com/popular*'),
                    HD=URL('https://www.thumbzilla.com/hd*'),
                    Homemade=URL('https://www.thumbzilla.com/homemade*'))

        view.add_start_button(picture_filename='model/site/resource/thumbzilla.png',
                              menu_items=menu_items,
                              url=URL("https://www.thumbzilla.com/newest*"))

    def get_shrink_name(self):
        return 'TZ'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        content=soup.find('section', id='content')
        if content:
            for thumbnail in _iter(content.find_all('a',{'class':'js-thumb'})):
                    href = URL(thumbnail.attrs['href'], base_url=url)

                    img=thumbnail.img
                    thumb_file=img.attrs.get('data-original',img.attrs.get('src'))
                    thumb_url = URL(thumb_file, base_url=url)

                    title = thumbnail.find('span',{'class':'title'})
                    label = '' if title is None else str(title.string).strip()

                    duration = thumbnail.find('span',{'class':'duration'})
                    dur_time = '' if duration is None else str(duration.string).strip()

                    hd_span = thumbnail.find('span', {'class': 'hd'})
                    hd = str(hd_span.string).strip() if hd_span else ''

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                                   labels=[{'text':dur_time, 'align':'top right'},
                                           {'text': hd, 'align': 'top left'},
                                           {'text':label, 'align':'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('section',{'class':'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        scripts = soup.find_all('script', text=lambda x: 'var pageVar =' in str(x))
        for script in _iter(scripts):
            videovars=quotes(str(script.string).replace(' ',''),"'videoVars':{","}").split(",")
            default=-1
            for var in videovars:
                (label,sep,href)=var.replace('"','').replace('\\','').partition(':')
                if label.startswith('quality_'):
                    if '720' in label:
                        default=len(self.video_data)
                    self.add_video(label, URL(href))
            self.set_default_video(default)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'class':'videoInfoTop'})
        if container:
            psp(container.prettify())
            stars=container.find('span',{'class':'stars'})
            if stars:
                for star in _iter(stars.find_all('a',href=True)):
                    self.add_tag(star.string,URL(star.attrs['href'],base_url=url),style=dict(color='red'))
            categories = container.find('span', {'class': 'categories'})
            if categories:
                for category in _iter(categories.find_all('a', href=True)):
                    self.add_tag(category.string, URL(category.attrs['href'], base_url=url))
            tags = container.find('span', {'class': 'tags'})
            if tags:
                for tag in _iter(tags.find_all('a', href=True)):
                    self.add_tag(tag.string, URL(tag.attrs['href'], base_url=url))

#
# class TZvideoSite(BaseSite):
#     def start_button_name(self):
#         return "TZvid"
#
#     def get_start_button_menu_text_url_dict(self):
#         return dict(Hottest=URL('https://www.thumbzilla.com/'),
#                     Newest=URL('https://www.thumbzilla.com/newest*'),
#                     Top=URL('https://www.thumbzilla.com/top*'),
#                     Trending=URL('https://www.thumbzilla.com/trending*'),
#                     Popular=URL('https://www.thumbzilla.com/popular*'),
#                     HD=URL('https://www.thumbzilla.com/hd*'),
#                     Homemade=URL('https://www.thumbzilla.com/homemade*'))
#
#     def startpage(self):
#         return URL("https://www.thumbzilla.com/newest*")
#
#     def can_accept_index_file(self, base_url=URL()):
#         return base_url.contain('thumbzilla.com/')
#
#     def get_href(self, txt='', base_url=URL()):
#         if txt.startswith('http://') or txt.startswith('https://'):
#             return txt
#         if txt.startswith('/'):
#             return 'https://' + base_url.domain() + txt
#         return ''
#
#     def parse_index_file(self, fname, base_url=URL()):
#         parser = SiteParser()
#
#         # print(base_url.domain())
#         def star_get_url(txt=''):
#             return txt.partition('(')[2].partition(')')[0]
#
#         startpage_rule = ParserRule(debug=False)
#         startpage_rule.add_activate_rule_level([('ul', 'class', 'responsiveListing')])
#         startpage_rule.add_process_rule_level('a', {'href'})
#         startpage_rule.add_process_rule_level('img', {'data-original'})
#         startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
#         startpage_rule.set_attribute_modifier_function('data-original', lambda x: x.replace('//', 'https://'))
#         parser.add_rule(startpage_rule)
#
#         startpage_pages_rule = ParserRule()
#         startpage_pages_rule.add_activate_rule_level([('section', 'class', 'pagination')])
#         # startpage_pages_rule.add_activate_rule_level([('a', 'class', 'current')])
#         startpage_pages_rule.add_process_rule_level('a', {'href'})
#         startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
#         parser.add_rule(startpage_pages_rule)
#
#         startpage_hrefs_rule = ParserRule()
#         startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'categoryList')])
#         # startpage_hrefs_rule.add_activate_rule_level([('a', 'class', 'current')])
#         startpage_hrefs_rule.add_process_rule_level('a', {'href'})
#         # startpage_hrefs_rule.add_process_rule_level('span', {''})
#         startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
#         parser.add_rule(startpage_hrefs_rule)
#         #
#         video_rule = ParserRule()
#         video_rule.add_activate_rule_level([('body', '', '')])
#         video_rule.add_process_rule_level('script', {})
#         video_rule.set_attribute_filter_function('data', lambda text: 'videoVars' in text)
#         parser.add_rule(video_rule)
#         #
#         gallery_href_rule = ParserRule()
#         gallery_href_rule.add_activate_rule_level([('div', 'class', 'videoInfoTop')])
#         # gallery_href_rule.add_activate_rule_level([('td', 'class', 'links')])
#         gallery_href_rule.add_process_rule_level('a', {'href'})
#         gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
#         # gallery_href_rule.set_attribute_filter_function('href',lambda x: x!='*')
#         parser.add_rule(gallery_href_rule)
#         #
#         # gallery_channel_rule = ParserRule()
#         # gallery_channel_rule.add_activate_rule_level([('p', 'class', 'source')])
#         # gallery_channel_rule.add_process_rule_level('a', {'href'})
#         # gallery_channel_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x + '*')
#         # parser.add_rule(gallery_channel_rule)
#
#         self.proceed_parcing(parser, fname)
#
#         result = ParseResult()
#
#         if len(video_rule.get_result()) > 0:
#             script = video_rule.get_result()[0]['data'].replace(' ', '')  # .replace('\\','')
#
#             # print(script)
#
#             urls = list()
#
#             while '"quality_' in script:
#                 nxt = script.partition('"quality_')[2]
#
#                 t = nxt.partition('":"')
#                 label = t[0]
#                 file = t[2].partition('",')[0].replace('%2F', '/').replace('%3F', '?').replace('%26', '&').replace(
#                     '%3D', '=')
#                 # print (label, file)
#                 urls.append(dict(text=label, url=URL('https:' + file + '*')))
#                 script = nxt
#
#             if len(urls) == 1:
#                 video = MediaData(urls[0]['url'])
#             elif len(urls) > 1:
#                 default = urls[len(urls) - 1]['url']
#                 for t in urls:
#                     if '720p' in t['text']:
#                         default = t['url']
#                 video = MediaData(default)
#                 for item in urls:
#                     video.add_alternate(item)
#             else:
#                 return result
#
#             result.set_type('video')
#             result.set_video(video)
#             #
#             # for f in gallery_channel_rule.get_result(['data', 'href']):
#             #     result.add_control(ControlInfo(f['data'], URL(f['href'])))
#
#             links = set()
#             for f in gallery_href_rule.get_result(['data', 'href']):
#                 if f['href'] not in links:
#                     label = f['data'].replace('\t', '')
#                     if label == '':
#                         label = f['href'].rpartition('/')[2]
#                     # print(f)
#                     result.add_control(ControlInfo(label, URL(f['href'])))
#                     links.add(f['href'])
#             return result
#
#         if len(startpage_rule.get_result()) > 0:
#             result.set_type('hrefs')
#
#             for item in startpage_rule.get_result(['href']):
#                 # print (item)
#                 result.add_thumb(ThumbInfo(thumb_url=URL(item['data-original']), href=URL(item['href']),
#                                            popup=item.get('title', '')))
#
#             for item in startpage_pages_rule.get_result(['href', 'data']):
#                 # print(item)
#                 result.add_page(ControlInfo(item['data'], URL(item['href'])))
#
#             if len(startpage_hrefs_rule.get_result(['href'])) > 0:
#                 for item in startpage_hrefs_rule.get_result(['href', 'data']):
#                     href = item['href']
#                     txt = href.rstrip('*').rpartition('/')[2]
#                     # print(item)
#                     result.add_control(ControlInfo(txt, URL(href)))
#
#         return result


if __name__ == "__main__":
    pass

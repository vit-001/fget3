# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter, quotes, psp
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.picture.base_of_tgp import TgpSite


class FuskatorSite(TgpSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('fuskator.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/picture/fuskator.png',
                              url=URL("http://fuskator.com/", test_string='Fuskator'))

    def get_shrink_name(self):
        return 'FK'

    def get_thumbs_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div', {'class':'thumblinks'})

    def get_thumbs_from_container(self, container: BeautifulSoup) -> list:
        return container.find_all('div',{'class':'pic'})

    def parse_one_thumb(self, thumbnail:BeautifulSoup, url:URL):
        psp(thumbnail.prettify())
        href_txt = thumbnail.attrs['href']
        if 'url=' in href_txt:
            href_txt = quotes(href_txt, 'url=', '&')
        href = URL(href_txt.strip('/')+'/')
        description = thumbnail.img.attrs.get('alt', '')
        if description is '':
            description = href_txt.strip('/').rpartition('/')[2].replace('-', ' ')
        thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
        # print(thumb_url,href,description)
        self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                       labels=[{'text': description, 'align': 'bottom center'}])

# class FKSite(BaseSite):
#     def start_button_name(self):
#         return "FK"
#
#     def startpage(self):
#         return URL("http://fuskator.com/")
#
#     def can_accept_index_file(self, base_url=URL()):
#         return base_url.contain('fuskator.com/')
#
#     def get_href(self, txt='', base_url=URL()):
#         if txt.startswith('http://') or txt.startswith('https://'):
#             return txt
#         if txt.startswith('/'):
#             return 'http://' + base_url.domain() + txt
#         return ''
#
#     def parse_index_file(self, fname, base_url=URL()):
#         # print(base_url)
#         parser = SiteParser()
#         startpage_rule = ParserRule()
#         startpage_rule.add_activate_rule_level([('div', 'class', 'thumblinks')])
#         # startpage_rule.add_process_rule_level('div', {})
#         startpage_rule.add_process_rule_level('a', {'href'})
#         startpage_rule.add_process_rule_level('img', {'src', 'alt'})
#         startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url) + '*')
#         startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url) + '*')
#         parser.add_rule(startpage_rule)
#
#         tags_rule = ParserRule()
#         tags_rule.add_activate_rule_level([('div', 'id', 'divTags')])
#         tags_rule.add_process_rule_level('a', {'href'})
#         tags_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
#         parser.add_rule(tags_rule)
#
#         startpage_pages_rule = ParserRule()
#         startpage_pages_rule.add_activate_rule_level([('td', 'class', 'pages')])
#         startpage_pages_rule.add_process_rule_level('a', {'href'})
#         startpage_pages_rule.set_attribute_modifier_function('href', lambda x: base_url.domain() + x)
#         parser.add_rule(startpage_pages_rule)
#
#         picture_base_addr_rule = ParserRule()
#         picture_base_addr_rule.add_activate_rule_level([('div', 'class', 'imagelinks')])
#         picture_base_addr_rule.add_process_rule_level('script', {})
#         picture_base_addr_rule.set_attribute_filter_function('data', lambda x: 'unescape' in x)
#         parser.add_rule(picture_base_addr_rule)
#
#         picture_rule = ParserRule()
#         picture_rule.add_activate_rule_level([('div', 'class', 'imagelinks')])
#         picture_rule.add_process_rule_level('script', {})
#         picture_rule.set_attribute_filter_function('data', lambda x: "'src'" in x)
#         parser.add_rule(picture_rule)
#
#         for s in open(fname):
#             parser.feed(s)
#
#         result = ParseResult()
#
#         if len(picture_base_addr_rule.get_result()) > 0:
#             result.set_type('pictures')
#             base = \
#             picture_base_addr_rule.get_result()[0]['data'].replace('%2f', '/').partition("unescape('//")[2].partition(
#                 "'")[0]
#             # print(base)
#             i = 1
#             for f in picture_rule.get_result():
#                 picname = f['data'].partition("+'")[2].partition("'")[0]
#                 # print(picname)
#                 result.add_full(FullPictureInfo(abs_href=URL(base + picname + '*'), rel_name='%03d.jpg' % i))
#                 i += 1
#
#             for item in tags_rule.get_result(['href', 'data']):
#                 result.add_control(ControlInfo(item['data'], URL(item['href'])))
#
#             return result
#
#         if len(startpage_rule.get_result()) > 0:
#             result.set_type('hrefs')
#             for item in startpage_rule.get_result():
#                 # print(item)
#                 result.add_thumb(
#                     ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']),
#                               popup=item.get('alt', '')))
#
#             for item in tags_rule.get_result(['href', 'data']):
#                 result.add_control(ControlInfo(item['data'], URL(item['href'])))
#
#             for item in startpage_pages_rule.get_result(['href', 'data']):
#                 result.add_page(ControlInfo(item['data'], URL(item['href'])))
#
#         return result


if __name__ == "__main__":
    pass
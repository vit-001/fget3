__author__ = 'Vit'

from base_classes import UrlList
from loader.old.multiprocess_loader import LoaderError
from loader.old.simple_loader import load
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class SXXvideoSite(BaseSite):
    def start_button_name(self):
        return "SXXvid"

    def startpage(self):
        return URL("http://sexix.net/?orderby=date*")

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('sexix.net/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        startpage_rule.add_activate_rule_level([('div', 'class', 'thumb')])
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_rule.add_process_rule_level('img', {'src', 'alt'})
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'class', 'wp-pagenavi')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        tags_rule = ParserRule()
        tags_rule.add_activate_rule_level([('div', 'class', 'tagcloud')])
        tags_rule.add_process_rule_level('a', {'href'})
        tags_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(tags_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'class', 'videoContainer')])
        video_rule.add_process_rule_level('iframe', {'src'})
        video_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_rule)

        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'id', 'extras')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():
            urls = UrlList()
            for item in video_rule.get_result():
                try:
                    r = load(URL(item['src']))
                    r = load(URL(self.quotes(r.text, "jwplayer().load('", "'") + '*'))
                    source = self.quotes(r.text, '<item>', '</item>').strip()
                    split = source.split('<jwplayer:source file="')
                    for l in split:
                        if l is '':
                            continue
                        url = l.partition('"')[0]
                        label = self.quotes(l, 'label="', '"')
                        urls.add(label, URL(url + '*'))

                except LoaderError as err:
                    print(err)

            result.set_video(urls.get_media_data())

            for f in gallery_href_rule.get_result(['data', 'href']):
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        if startpage_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            for item in startpage_rule.get_result(['href']):
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('alt', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                result.add_page(ControlInfo(item['data'], URL(item['href'])))

            for item in tags_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass

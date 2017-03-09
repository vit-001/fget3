__author__ = 'Vit'

from loader.old.simple_loader import load
from site_models.base_site_model import *
from site_models.site_parser import SiteParser, ParserRule


class YPvideoSite(BaseSite):
    def start_button_name(self):
        return "YPvid"

    def get_start_button_menu_text_url_dict(self):
        return dict(Latest=URL('http://yourporn.sexy/blog/all/0.html?sm=latest*'),
                    Views=URL('http://yourporn.sexy/blog/all/0.html?sm=views*'),
                    Rating=URL('http://yourporn.sexy/blog/all/0.html?sm=rating*'),
                    Orgazmic=URL('http://yourporn.sexy/blog/all/0.html?sm=orgasmic*'),
                    )

    def startpage(self):
        return URL("http://yourporn.sexy/blog/all/0.html*", test_string='YourPorn')

    def can_accept_index_file(self, base_url=URL()):
        return base_url.contain('yourporn.sexy/')

    def parse_index_file(self, fname, base_url=URL()):
        parser = SiteParser()

        startpage_rule = ParserRule()
        # startpage_rule.add_activate_rule_level([('div', 'class', 'post_block')])#
        startpage_rule.add_activate_rule_level([('div', 'class', 'vid_container')])  #
        startpage_rule.add_process_rule_level('img', {'src'})
        startpage_rule.add_process_rule_level('a', {'href', 'title'})
        # startpage_rule.set_attribute_filter_function('src',lambda x: '.jpg' in x)
        startpage_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        # startpage_rule.set_attribute_modifier_function('title', lambda x: x.partition('#')[0])
        parser.add_rule(startpage_rule)

        startpage_combo_rule = ParserRule()
        # startpage_rule.add_activate_rule_level([('div', 'class', 'post_block')])#
        startpage_combo_rule.add_activate_rule_level([('div', 'class', 'combo_post_wrap')])
        startpage_combo_rule.add_process_rule_level('a', {'href', 'title'})
        startpage_combo_rule.add_process_rule_level('img', {'src'})
        # startpage_rule.set_attribute_filter_function('src',lambda x: '.jpg' in x)
        # startpage_combo_rule.set_attribute_modifier_function('title', lambda x: x.partition('#')[0])
        startpage_combo_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        startpage_combo_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_combo_rule)

        startpage_pages_rule = ParserRule()
        startpage_pages_rule.add_activate_rule_level([('div', 'id', 'center_control')])
        startpage_pages_rule.add_process_rule_level('a', {'href'})
        startpage_pages_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_pages_rule)

        startpage_hrefs_rule = ParserRule()
        startpage_hrefs_rule.add_activate_rule_level([('ul', 'class', 'dropdown-menu columns')])
        startpage_hrefs_rule.add_process_rule_level('a', {'href'})
        # startpage_hrefs_rule.set_attribute_filter_function('href',lambda x: '/channel/' in x or '/prime/' in x)
        startpage_hrefs_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(startpage_hrefs_rule)

        video_rule = ParserRule()
        video_rule.add_activate_rule_level([('div', 'itemprop', 'video')])
        # video_rule.add_process_rule_level('a', {'href'})
        video_rule.add_process_rule_level('video', {'src'})
        video_rule.set_attribute_modifier_function('src', lambda x: self.get_href(x, base_url))
        parser.add_rule(video_rule)

        video_multipart_rule = ParserRule()
        video_multipart_rule.add_activate_rule_level([('div', 'id', 'videos_container')])
        # video_rule.add_process_rule_level('a', {'href'})
        video_multipart_rule.add_process_rule_level('div',
                                                    {'data-source', 'data-hash', 'data-x', 'data-oid', 'data-pid'})
        parser.add_rule(video_multipart_rule)

        video_usss_rule = ParserRule()
        video_usss_rule.add_activate_rule_level([('body', '', '')])
        # video_rule.add_process_rule_level('a', {'href'})
        video_usss_rule.add_process_rule_level('script', {})
        video_usss_rule.set_attribute_filter_function('data', lambda x: 'usss' in x)
        parser.add_rule(video_usss_rule)

        #
        gallery_href_rule = ParserRule()
        gallery_href_rule.add_activate_rule_level([('div', 'class', 'popular_block_header_rl')])
        gallery_href_rule.add_process_rule_level('a', {'href'})
        # gallery_href_rule.set_attribute_filter_function('href',lambda x: '#' not in x)
        gallery_href_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_href_rule)

        gallery_author_rule = ParserRule()
        gallery_author_rule.add_activate_rule_level([('div', 'id', 'posts_container')])  # post_block
        gallery_author_rule.add_activate_rule_level([('div', 'class', 'post_author_name')])  # post_block
        gallery_author_rule.add_process_rule_level('a', {'href'})
        # gallery_href_rule.set_attribute_filter_function('href',lambda x: '#' not in x)
        gallery_author_rule.set_attribute_modifier_function('href', lambda x: self.get_href(x, base_url))
        parser.add_rule(gallery_author_rule)

        self.proceed_parcing(parser, fname)

        result = ParseResult()

        if video_rule.is_result():  # len(video_rule.get_result()) > 0:
            # print('video rule')
            # print(video_rule.get_result())

            video = MediaData(URL(video_rule.get_result()[0]['src']))

            # result.set_type('video')
            result.set_video(video)

            for f in gallery_author_rule.get_result(['data', 'href']):
                # print(f)
                result.add_control(ControlInfo('"' + f['data'].strip() + '"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                # print(f)
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        if video_multipart_rule.is_result():

            res = video_multipart_rule.get_result()
            series = len(res)

            s = base_url.get().partition('?s=')[2]

            if s == '':
                serie = 1
            else:
                serie = int(s)

            uid = self.quotes(video_usss_rule.get_result()[0]['data'].replace(' ', ''), 'usss[0]="', '"')
            curr_result = res[serie - 1]

            data = {'uid': uid, 'source': curr_result['data-source'], 'hash': curr_result['data-hash'],
                    'x': curr_result['data-x'],
                    'oid': curr_result['data-oid'], 'pid': curr_result['data-pid']}

            url = URL(self.get_href('/php/get_vlink.php', base_url), 'POST', post_data=data)

            r = load(url)

            video = MediaData(URL(r.text))

            result.set_type('video')
            result.set_video(video)

            for i in range(1, series + 1):
                label = 'S{0}'.format(i)
                if i == serie:
                    label += '(this)'
                url_i = base_url.get().partition('?')[0] + '?s={0}'.format(i)
                result.add_control(ControlInfo(label, URL(url_i + '*')))

            for f in gallery_author_rule.get_result(['data', 'href']):
                # print(f)
                result.add_control(ControlInfo('"' + f['data'].strip() + '"', URL(f['href'])))

            for f in gallery_href_rule.get_result(['data', 'href']):
                # print(f)
                result.add_control(ControlInfo(f['data'].strip(), URL(f['href'])))
            return result

        if startpage_rule.is_result() or startpage_combo_rule.is_result():  # len(startpage_rule.get_result()) > 0:
            # result.set_type('hrefs')

            for item in startpage_combo_rule.get_result():
                print(item)
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('title', '')))

            for item in startpage_rule.get_result(['href']):
                print(item)
                result.add_thumb(
                    ThumbInfo(thumb_url=URL(item['src']), href=URL(item['href']), popup=item.get('title', '')))

            for item in startpage_pages_rule.get_result(['href', 'data']):
                href = item['href']
                data = item['data']
                n = href.rpartition('/')[2].partition('.')[0]
                result.add_page(ControlInfo('{1}'.format(data, n), URL(href)))

            for item in startpage_hrefs_rule.get_result(['href', 'data']):
                result.add_control(ControlInfo(item['data'], URL(item['href'])))

        return result


if __name__ == "__main__":
    pass

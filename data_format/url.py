# -*- coding: utf-8 -*-
__author__ = 'Nikitin'


from urllib.parse import urlparse, urlsplit, parse_qs, parse_qsl, urlencode, urlunsplit, SplitResult

def get_href(txt: str, base_url):
    txt = txt.strip()
    if txt.startswith('http://'):
        return txt
    if txt.startswith('https://'):
        return txt
    if txt.startswith('//'):
        return base_url.scheme() + ':'+ txt
    if txt.startswith('/'):
        return base_url.scheme() +'://'+ base_url.domain() + txt
    return base_url.get().rpartition('/')[0] + '/' + txt

class URL:
    SUFFIXES = ['.html', '.jpg', '.gif', '.JPG', '.mp4', '.flv', 'png']
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"

    def __init__(self,
                 url='',
                 method='GET',
                 base_url=None,

                 coockies=None,
                 user_agent=None,
                 referer=None,
                 post_data=None,
                 any_data=None,

                 load_method=None,
                 forced_proxy=False,
                 forced_unproxy=False,
                 test_string=None,
                 ):

        self.method = method
        self.coockies = coockies
        self._user_agent = user_agent
        self.referer = referer
        self.post_data = post_data
        self.any_data = any_data
        self.load_method=load_method
        self.forced_proxy = forced_proxy
        self.forced_unproxy = forced_unproxy
        self.test_string = test_string

        if base_url:
            url = get_href(url, base_url)

        if url == '':
            self.url = ''
            self.no_slash = True
            return

        if url.startswith('//'):
            url = 'http:' + url

        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        if url.endswith('*') or not url.endswith('/'):
            self.no_slash = True
            url = url.rstrip('*')
        else:
            self.no_slash=False

        for suffix in URL.SUFFIXES:
            if url.lower().endswith(suffix):
                self.no_slash=True

        self.url=url


    def get(self):
        if self.no_slash:
            return self.url.rstrip('/')
        return self.url.rstrip('/') + '/'

    def get_short_filename(self, base=''):
        p = urlparse(self.get())
        return base.rstrip('/') + '/' + p[1] + '/' + p[2].strip(' /').replace('/', '..')

    def get_path(self, base=''):
        p = urlparse(self.get())
        p2 = p[2]
        if p2.endswith('.html') or p2.endswith('.jpg'):
            p2 = p2.rpartition('/')[0] + '/'
        return base.rstrip('/') + '/' + p[1] + p2.rstrip('/') + '/'

    def domain(self):
        return  urlparse(self.get())[1]

    def scheme(self):
        return urlsplit(self.get())[0]

    def contain(self, text:str):
        return text in self.url

    def add_query(self, pair_list):
        split = urlsplit(self.url)
        qs = parse_qs(split[3]).keys()
        qsl = parse_qsl(split[3])

        added = set()
        for (add_name, add_value) in pair_list:
            if add_name not in qs:
                added.add(add_name)

        new_qsl = list()
        for (name, value) in qsl:
            for (add_name, add_value) in pair_list:
                if add_name == name:
                    value = add_value
            new_qsl.append(tuple([name, value]))
        for (add_name, add_value) in pair_list:
            if add_name in added:
                new_qsl.append(tuple([add_name, add_value]))

        new_query = urlencode(new_qsl)
        self.url = urlunsplit(SplitResult(scheme=split[0], netloc=split[1], path=split[2], query=new_query, fragment=split[4]))

    @property
    def user_agent(self)-> str:
        if self._user_agent:
            return self._user_agent
        else:
            return URL.USER_AGENT

    def link(self):
        return '<a href="'+ self.get()+'">'+self.get() +'</a>'

    def __repr__(self, *args, **kwargs):
        return '<URL:'+self.get()+'>'

    def __str__(self, *args, **kwargs):
        return self.get()

    def __eq__(self, url2):
        # print('Compare', self,url2)
        if url2 is None:
            return False
        if self.method != url2.method:
            return False
        if self.method == 'GET':
            return url2.get() == self.get()
        elif self.method == 'POST':
            if url2.get() != self.get():
                return False
            if self.post_data is None:
                return url2.post_data is None
            if url2.post_data is None:
                return False
            for key in self.post_data:
                if self.post_data[key] != url2.post_data[key]:
                    return False
            for key in url2.post_data:
                if self.post_data[key] != url2.post_data[key]:
                    return False
            return True
        return False

    def to_dict_serialize(self)->dict:
        return dict(url=self.get())

    @staticmethod
    def from_dict(data:dict):
        return URL(url=data.get('url',''),
                   )



if __name__ == "__main__":
    url1=URL('https://yourporn.sexy/blog/all/0.html')
    url2=URL('/post/58c7c669574dc.html', base_url=url1)

    print(url2)
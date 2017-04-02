# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions


def load(url, fname, cookies=None, headers=None, proxies=None):
    print('Loading', url, 'to', fname)
    try:
        response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies)
        response.raise_for_status()
        with open(fname, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)



    except requests.exceptions.HTTPError as err:
        print('HTTP error: {0}'.format(err.response.status_code))
        # return response

    except requests.exceptions.ConnectTimeout:
        print('Connection timeout')

    except requests.exceptions.ReadTimeout:
        print('Read timeout')

    except requests.exceptions.ConnectionError:
        print('Connection error')

    except:
        print('Unknown error in loader')
    else:
        print('loaded ok!')
        return response

def get_response(url, fname, cookies=None, headers=None, proxies=None):
    print('Loading', url, 'to', fname)
    try:
        response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, stream=True, allow_redirects=False)
        response.raise_for_status()
        # with open(fname, 'wb') as fd:
        #     for chunk in response.iter_content(chunk_size=128):
        #         fd.write(chunk)



    except requests.exceptions.HTTPError as err:
        print('HTTP error: {0}'.format(err.response.status_code))
        # return response

    except requests.exceptions.ConnectTimeout:
        print('Connection timeout')

    except requests.exceptions.ReadTimeout:
        print('Read timeout')

    except requests.exceptions.ConnectionError:
        print('Connection error')

    except:
        print('Unknown error in loader')
    else:
        print('loaded ok!')
        print(response.headers.get('Location', 'ne redirect'))

        return response


if __name__ == "__main__":

    proxies={'http': 'proxy.antizapret.prostovpn.org:3128'}

    url1 = 'https://beemtube.com/most-recent/'
    url1a = 'https://www.vporn.com/pov/big-tits-round-asses/1727606/?t=1'
    url2 = 'https://pornfun.com/get_file/1/ee2513bd5c65836da1a9bd7c3c5f8fbb/27000/27100/27100.mp4'
    url3 = 'http://www4.pornfun.com/remote_control.php?time=1490688627&cv=cb90ade678228733e045b68465b6f1a6&lr=0&cv2=c1451132bb5e338af902bc1c75302b82&file=%2Fcontents%2Fvideos%2F27000%2F27100%2F27100.mp4&cv3=becb9c8a2b412ea8f3fe2e3541341d4b'

    fname1 = 'out/1.html'
    fname1a = 'out/1a.html'
    fname1b = 'out/1b.html'
    fname1c = 'out/1.html'
    fname2 = 'out/1.mp4'
    fname2a = 'out/2.html'
    fname3 = 'out/3.json'
    fname4 = 'out/1.js'


    # coockies={'_gat':'1', 'protect':'BPJvGkuwOdy0D4amF44YTA', '_ga':'GA1.2.638382635.1487974825'}

    # headers = {'Referer': 'http://her69.net/massagerooms-daphne-angel-daisy-lee/'}

    # r=load(url1,fname1)#, proxies=proxies)
    # r = load(url2, fname2)
    # r = load(url1a, fname1a, proxies=proxies)
    r = load(url1a, fname1a)
    # r = load(url2, fname2)#, proxies=proxies)

    # r=get_response(url3, fname2)

    # r=load('https://assets.porndig.com/assets/porndig/js/bundle.js?ver=1481122807','e:/out/bundle.js')

    print(r.status_code)
    print(r.history)

    for item in r.headers:
        print(item, ':', r.headers[item])

    print('========request========')
    for item in r.request.headers:
        print(item, ':', r.request.headers[item])
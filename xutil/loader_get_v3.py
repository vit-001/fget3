# -*- coding: utf-8 -*-
__author__ = 'Vit'
import requests
import requests.exceptions



def load(url, fname, cookies=None, headers=None, proxies=None):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"

    print('Loading', url, 'to', fname)
    try:
        if not headers:
            headers = dict()
        headers['user-agent'] = USER_AGENT

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


    url1 = 'https://sickjunk.com/'
    url1a = 'https://rt.pornhub.com/view_video.php?viewkey=ph5ffb20cb5d07b'
    url2 = 'https://www.eporner.com/embed/i9EKB71E49b/'
    url3 = 'https://cdn8.bdsmstreak.com/hd/47063.mp4?md5=VuDNvEj9XqZ0z-VX768BGQ&expires=1626253427'


    fname1 = 'out/1.html'
    fname1a = 'out/1a.html'
    fname1b = 'out/1b.html'
    fname1c = 'out/1.html'
    fname2 = 'out/1.mp4'
    fname2a = 'out/2.html'
    fname3 = 'out/3.json'
    fname4 = 'out/1.js'
    fname5 = 'out/1.svg'
#PHPSESSID=b5452159d9b0465182078eaecf8c7dcf; kt_ips=217.66.158.229; _ga=GA1.2.1348248477.1626100592; _gid=GA1.2.1906675378.1626100592; kt_tcookie=1; fapsterp0=1; _stat=3965542467.2905627009.23479322.3785358264; _gat_gtag_UA_135268328_1=1

    coockies={'PHPSESSID':'b5452159d9b0465182078eaecf8c7dcf',
    }

    headers = {'Referer': 'https://bdsmstreak.com/'}

    # r=load(url1,fname1)#, proxies=proxies)
    # r = load(url2, fname1b)#,headers=headers)
    # r = load(url1a, fname1a, proxies=proxies)
    r = load(url1a, fname1a)#, cookies=coockies)
    # r = load(url3, fname2, cookies=coockies,headers=headers)#, proxies=proxies)


    # r=get_response(url3, fname2)

    # r=load('https://assets.porndig.com/assets/porndig/js/bundle.js?ver=1481122807','e:/out/bundle.js')

    print(r)
    print(r.status_code)
    print(r.history)

    for item in r.headers:
        print(item, ':', r.headers[item])

    print('========request========')
    for item in r.request.headers:
        print(item, ':', r.request.headers[item])

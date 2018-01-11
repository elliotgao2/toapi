from toapi import Css, Item, Api, Settings


class MySettingd(Settings):
    web = {
        "with_ajax": False,
        "request_config": {
            'headers': {
                'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"
            }
        },
        "headers": None
    }


api = Api()


class Bing(Item):
    __name__ = 'bing'
    __base_url__ = 'https://www.bing.com'

    url = Css('h2 a', attr='href')
    title = Css('h2 a')

    def clean_url(self, url):
        if isinstance(url, list):
            url = url[0].get('href')
        return url

    def clean_title(self, title):
        if isinstance(title, list):
            text = ''
            for node in title[0].itertext():
                text += node
            title = text.strip()
        return title

    class Meta:
        source = Css('li.b_algo')
        route = {'/:wd': '/search?q=:wd&ensearch=1'}


class Baidu(Bing):
    __name__ = 'baidu'
    __base_url__ = 'http://www.baidu.com'

    url = Css('h3.t a', attr='href')
    title = Css('h3.t a')

    class Meta:
        source = Css('div.result')
        route = {'/:wd': '/s?wd=:wd&ie=utf-8&vf_bl=1'}


api.register(Baidu)
api.register(Bing)

if __name__ == '__main__':
    print(api.parse('/python'))
    api.serve()

    # Visit http://127.0.0.1:5000/python

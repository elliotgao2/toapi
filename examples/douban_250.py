from toapi import Css, Item, Api

try:
    bool(type(unicode))
except NameError:
    unicode = str

api = Api('https://movie.douban.com/top250')


class Post(Item):
    url = Css('div.hd>a', attr='href')
    title = Css('span.title')

    class Meta:
        """
        URL: http://127.0.0.1:5000/250/
        Des: 豆瓣250电影api
        Params:
            start: eg: http://127.0.0.1:5000/250/?start=25
        """
        source = Css('div.item', attr='target')
        route = (
            ('/250/?start=:start', '/?start=:start'),
            ('/250/', '/')
        )

    def clean_title(self, title):
        if isinstance(title, unicode):
            return title.replace(u'\xa0', '')
        else:
            return ''.join([i.text.strip().replace(u'\xa0', '') for i in title])

    def clean_url(self, value):
        return value


api.register(Post)

if __name__ == '__main__':
    headers = {
        'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"
    }
    print(api.parse('/250/?start=25', headers=headers))
    api.serve()
    # Visit http://127.0.0.1:5000/250/
    # http://127.0.0.1:5000/250/?start=25
    # http://127.0.0.1:5000/250/?start=50
    # ...

"""
{
    "post": [
        {
            "title": "肖申克的救赎/The Shawshank Redemption",
            "url": "https://movie.douban.com/subject/1292052/"
        },
        {
            "title": "霸王别姬",
            "url": "https://movie.douban.com/subject/1291546/"
        },
        {
            "title": "这个杀手不太冷/Léon",
            "url": "https://movie.douban.com/subject/1295644/"
        }
    ]
}
"""

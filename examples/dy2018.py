from toapi import XPath, Item, Api

api = Api(base_url='http://www.dy2018.com')


class MovieList(Item):
    url = XPath('//b//a[@class="ulink"]/@href')
    title = XPath('//b//a[@class="ulink"]/text()')

    class Meta:
        source = XPath('//table[@class="tbspan"]')
        route = {'/movies/?page=1': '/html/gndy/dyzz/',
                 '/movies/?page=:page': '/html/gndy/dyzz/index_:page.html',
                 '/movies/': '/html/gndy/dyzz/'}

    def clean_url(self, url):
        return '/movies/{}/'.format(url.split('/')[-1].split('.')[0])


class Movie(Item):
    download = XPath('//*[@id="Zoom"]/table[1]//a/text()')

    class Meta:
        source = None
        route = {'/movies/:id': '/i/:id.html'}


api.register(MovieList)
api.register(Movie)

api.serve()

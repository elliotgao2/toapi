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

if __name__ == '__main__':
    import time

    start = time.time()
    # 10000  Time: 3.6778430938720703  Time: 3.0024631023406982
    # 100000 Time: 40.471128940582275  Time: 31.377354860305786
    # for i in range(100000):
    #     api.parse('/movies/?page=2')
    # print("Time: {}".format(time.time() - start))
    api.serve()

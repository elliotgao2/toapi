from flask import jsonify, request

from toapi import XPath, Item, Api

api = Api(base_url='http://www.dy2018.com')


class MovieList(Item):
    url = XPath('//b//a[@class="ulink"]/@href')
    title = XPath('//b//a[@class="ulink"]/text()')

    class Meta:
        source = XPath('//table[@class="tbspan"]')
        route = '/html/gndy/dyzz/(index_\d+.html)?'

    def clean_url(self, url):
        return '/movies/{}/'.format(url.split('/')[-1].split('.')[0])


class Movie(Item):
    download = XPath('//*[@id="Zoom"]/table[1]//a/text()')

    class Meta:
        source = None
        route = '/i/\d+.html'


api.register(MovieList)
api.register(Movie)
app = api.server.app


@app.route('/movies/')
def movie_list():
    page = request.args.get('page', '1')
    results = {}
    results['page'] = {
        'next': '/movies/?page={}'.format(int(page) + 1) if int(page) > 0 else None,
        'prev': '/movies/?page={}'.format(int(page) - 1) if int(page) > 1 else None
    }
    if page == '1':
        results['data'] = api.parse('/html/gndy/dyzz/')
    else:
        results['data'] = api.parse('/html/gndy/dyzz/index_{}.html'.format(page))
    return jsonify(results)


@app.route('/movies/<id>/')
def movie(id):
    return jsonify(api.parse('/i/{}.html'.format(id)))


api.serve()

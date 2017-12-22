from toapi import Api


def test_alias():
    api = Api()
    assert api.convert_route_to_alias('/movies/22/?output=utf-8',
                                      '/movies/\d{1,2}/?output=:page',
                                      '/movies/test/:page.html') == '/movies/test/utf-8.html'

    assert api.convert_route_to_alias('/movies/22/?你好=你好',
                                      '/movies/\d{1,2}/?你好=:page',
                                      '/movies/test/:page.html') == '/movies/test/你好.html'

    assert api.convert_route_to_alias('/movies/22/?page=2',
                                      '/movies/\d{1,2}/?page=:page',
                                      '/movies/test/index_:page.html') == '/movies/test/index_2.html'

    assert api.convert_route_to_alias('/movies/?page=2',
                                      '/movies/?page=:page',
                                      '/html/gndy/dyzz/index_:page.html') == '/html/gndy/dyzz/index_2.html'

    assert api.convert_route_to_alias('/movies/you/?page=2',
                                      '/movies/:fuck/?page=:page',
                                      '/html/gndy/:fuck/index_:page.html') == '/html/gndy/you/index_2.html'


    assert api.convert_route_to_alias('/movies/you/?page=2&a=1',
                                      '/:path',
                                      '/:path') == '/movies/you/?page=2&a=1'


    assert api.convert_route_to_alias('/',
                                      '/',
                                      '/') == '/'


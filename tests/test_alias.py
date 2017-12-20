from toapi import Api


def test_alias():
    api = Api()
    assert api.convert_route_to_alias('/movies/?page=2',
                                      '/movies/?page=:page',
                                      '/html/gndy/dyzz/index_:page.html') == '/html/gndy/dyzz/index_2.html'

    assert api.convert_route_to_alias('/movies/you/?page=2',
                                      '/movies/:fuck/?page=:page',
                                      '/html/gndy/:fuck/index_:page.html') == '/html/gndy/you/index_2.html'



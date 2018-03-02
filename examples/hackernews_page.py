from htmlparsing import Attr, Text

from toapi import Api, Item

api = Api('https://news.ycombinator.com/')


@api.list('.athing')
@api.route(['/post?p={page}', '/news?p={page}'])
class Post(Item):
    url = Attr('.storylink', 'href')
    title = Text('.storylink')


@api.route(['/post?p={page}', '/news?p={page}'])
class Page(Item):
    next_page = Attr('.morelink', 'href')


api.app.run(debug=True, host='0.0.0.0', port=5000)

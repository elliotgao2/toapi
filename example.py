from .toapi import Css, XPath, Regex, Item, Api

api = Api('https://news.ycombinator.com/')


class Post(Item):
    title = Css()
    url = XPath()
    author = Regex()

    class Meta:
        source = Css()
        list = True


class Comment(Item):
    title = Css()

    class Meta:
        source = Css()
        list = True


class User(Item):
    username = Css()
    karma = XPath()

    class Meta:
        source = XPath()
        list = True


api.route('/', [Post, Comment])
api.route('/user?id=/\.+/', User)

print(api.parse('/'))
print(api.parse('/user?id=gaojiuli'))

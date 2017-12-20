Item is the key to the whole system which determine what is the result and
where is the result. 

```python
from toapi import XPath, Item

class MovieList(Item):
    __base_url__ = 'http://www.dy2018.com'
    
    url = XPath('//b//a[@class="ulink"]/@href')
    title = XPath('//b//a[@class="ulink"]/text()')

    class Meta:
        source = XPath('//table[@class="tbspan"]')
        route = '/html/gndy/dyzz/index_:page.html'
        alias = '/movies/?page=:page'
```

When you visit `http://127.0.0.1:/movies/?page=2`, You could get the item from `http://www.dy2018.com/html/gndy/dyzz/index_2.html`

As you can see. The fields of item are [selector instances](selector). 
And the Meta class determine the basic attributes of item.

- Meta.source: A section of a HTML, which should contains one complete item. It is a [selector instance](selector)
- Meta.route: The url path regex expression of source site.
- Meta.alias: Defining the api server route. Determine how to access the item.
 
## Clean Data

The `clean_{field}` method of item instance is for further processing the returned values. For example:

```python
from toapi import XPath, Item

class Post(Item):
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'
        
    def clean_url(self, url):
        return 'http://127.0.0.1%s' % url
```
Item is the key to the whole system which determine what is the result and
where is the result. 

```python
from toapi import XPath, Item

class Post(Item):
    url = XPath('//a[@class="storylink"]/@href')
    title = XPath('//a[@class="storylink"]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'
```

As you can see. The fields of item are [selector instances](selector). 
And the Meta class determine the basic attributes of item.

- Meta.source: A section of a HTML, which should contains one complete item. It is a [selector instance](selector)
- Meta.route: The url path regex expression of source site.

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
Storage provides 2 ways to you to store your data -- local disk and database.

## How to configure them

### Local Disk
Your data will be stored in a hidden file called .html which will be created in where programe running.  
You can still input the path you want to store in Settings.  

```python
from toapi import Api, Settings


class MySettings(Setting):
    '''your own settings'''

    storage = {
        "PATH": "/Users/username/toapi",
        "DB_URL": None
    }  
```
Sytem will load your path, and create a hidden file -- .html under your path: /Users/username/toapi/.html, and every site will be stored here.

### Database
You need a database to save your import data and make it read faster.  
To use database, you have to configure it first.

```python
from toapi import Api, Settings


class MySettings(Setting):
    '''your own settings'''

    storage = {
        "PATH": "/Users/username/toapi",
        "DB_URL": "sqlite:////User/username/toapi/data.sqlite"
    }
```
warning: if you configure PATH and DB_URL both, system will use database only!


## How to use storage

It‘s easy and cheeryful to use it, you even do not configure anything.
```python
from storage import Storage
from api import Settings

store = Storage(Settings)
url = "www.toapi.org"
html = "html content"
store.save(url, html)
store.get(url) # you can give a expiration
```

## Attributes

### save(url, html)
save() receive two params, url and html.  
- url is the url you current surf
- html is the contents you current surf.

### get(url, default, expiration)
get() receive three params, url, default and expiration.  
- url is easy and simple to know.  
- default is the returned value while no result finding in disk or database.
- expiration means you want to get the contents in expired time, if data expired, the system will automatically delete.

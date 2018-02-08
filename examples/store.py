from toapi.storage import Storage
from time import time, sleep
import os

# store = DiskStore()

url = "https://www.google.com"
html = "<p> Hello, World!</p>"


# store.save(url, html)
# print(store.get(url))


class Settings:
    """Global Settings"""
    storage = {
        "PATH": os.getcwd(),
        "DB_URL": None,
        "EXPIRATION": 5
    }


class Settings2:
    """Global Settings"""
    storage = {
        "PATH": os.getcwd(),
        "DB_URL": "mysql://thys:123456@localhost/order_system",
        "EXPIRATION": 5
    }


def time_it(f):
    def decorator(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print("uses time: {}s".format(time() - t))
        return res

    return decorator


@time_it
def io_test():
    url = "https://www.google.com"
    html = "<p> Hello, World!</p>\n<h1>this is a big problem</h1>"
    store = Storage(Settings)
    # for i in range(10000):
    #     url = url+str(i)
    #     store.get(url)
    store.get("ssssss")


def disk_test():
    url = "https://www.google.com123"
    html = "<p>你好世界</p>\n<h1>this is a b'ig problem</h1'>"
    store = Storage(settings=Settings)
    n = 1
    # while n < 3:
    #     store.save(url, html)
    #     sleep(10)
    #     print("times: {}".format(n))
    #     n += 1
    store.save(url, html)
    sleep(6)
    print(store.get(url))


def db_store():
    url = "测试中文"
    html = "中文测试<a>add html</a><p>add a\'</p>"
    store = Storage(Settings2)
    store.save(url, html)
    sleep(6)
    print(store.get(url))


if __name__ == "__main__":
    # io_test()
    # disk_test()
    db_store()

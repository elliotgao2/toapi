from toapi.storage import DiskStore, DBStore
from time import time
# store = DiskStore()

url = "https://www.google.com"
html = "<p> Hello, World!</p>"
# store.save(url, html)
# print(store.get(url))


def time_it(f):
    def decorator(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print("uses time: {}s".format(time()-t))
        return res
    return decorator


@time_it
def io_test():
    url = "https://www.google.com"
    html = "<p> Hello, World!</p>\n<h1>this is a big problem</h1>"
    store = DiskStore()
    # for i in range(10000):
    #     url = url+str(i)
    #     store.get(url)
    store.get("ssssss")


def disk_test():
    url = "https://www.google.com123"
    html = "<p> Hello, 'World!</p>\n<h1>this is a b'ig problem</h1'>"
    store = DiskStore()
    # store.save(url, html)
    print(store.get(url, expiration=5))


def db_store():
    url = "https://www.google.com"
    html = "<p> Hello, 'World!</p>\n<h1>this is a b'ig problem</h1'>"
    storage = {
        "DB_URL": "mysql://thys:123456@localhost/order_system"
    }
    store = DBStore(storage)
    # store.save(url, html)
    print(store.get(url, expiration=5))


if __name__ == "__main__":
    # io_test()
    # disk_test()
    db_store()


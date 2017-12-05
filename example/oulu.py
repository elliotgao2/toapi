from toapi import Api, XPath, Item

api = Api('http://my.eudic.net/recite/userbooks')

api.login('http://dict.eudic.net/Account/Login?returnUrl=', data={'UserName': 'hjlarry@163.com', 'Password': '123456aa'})


class MyBooks(Item):
    bookname = XPath('.//h3[@class="panel-title"]/text()')
    introduction = XPath('.//small[@class="book_small_text"]/text()')
    date = XPath('.//div[@class="panel-foot"]/text()')

    class Meta:
        source = XPath('//div[@class="eq-height"]/div')
        route = '/'


api.register(MyBooks)

api.serve()

# Visit http://127.0.0.1:5000/

"""
{
  "mybooks": [
    {
      "bookname": "\u6cd5\u8bed\u8bfe\u672c", 
      "date": "\r\n                                    2017\u5e7412\u670805\u65e5\r\n                                ", 
      "introduction": "I don't let myself start a book that I'm not gonna finish.\n\u5982\u679c\u6211\u77e5\u9053\u8fd9\u672c\u4e66\u6211\u8bfb\u4e0d\u5b8c\uff0c\u6211\u5c31\u4e0d\u4f1a\u53bb\u770b"
    }, 
    {
      "bookname": "\u82f1\u8bed\u8bfe\u672c", 
      "date": "\r\n                                    2017\u5e7412\u670805\u65e5\r\n                                ", 
      "introduction": "\u4e13\u4e1a\u82f1\u8bed\u8bfe\u6587\u9605\u8bfb"
    }, 
    {
      "bookname": "\u8bed\u6587\u8bfe\u672c", 
      "date": "\r\n                                    2017\u5e7412\u670805\u65e5\r\n                                ", 
      "introduction": "\u611f\u6168\u554a\uff0c\u53ea\u662f\u4e00\u4e2a\u666e\u901a\u611f\u5192\u800c\u5df2\uff0c\u5c45\u7136\u7ed9\u5b69\u5b50\u5f00\u4e86 5 \u79cd\u836f\u2026\u2026\u6839\u636e\u5b69\u5b50\u5f53\u65f6\u7684\u72b6\u6001\uff0c\u5b8c\u5168\u6ca1\u5fc5\u8981\u5403\u8fd9\u4e9b\u836f\u3002\u6d4b\u8bd5\u4e00\u4e0b\u554a"
    }
  ]
}

"""
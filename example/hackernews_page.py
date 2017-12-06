from toapi import XPath, Item, Api

api = Api('https://news.ycombinator.com/', with_ajax=True)


class Post(Item):
    url = XPath('//a[@class="storylink"][1]/@href')
    title = XPath('//a[@class="storylink"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/news\?p=\d+'


class Page(Item):
    next_page = XPath('//a[@class="morelink"]/@href')

    class Meta:
        source = None
        route = '/news\?p=\d+'

    def clean_next_page(self, next_page):
        return "http://127.0.0.1:5000/" + next_page


api.register(Post)
api.register(Page)

api.serve()

# Visit http://127.0.0.1:5000/news?p=1

"""
{
  "page": {
    "next_page": "http://127.0.0.1:5000/news?p=2"
  },
  "post": [
    {
      "title": "IPvlan overlay-free Kubernetes Networking in AWS", 
      "url": "https://eng.lyft.com/announcing-cni-ipvlan-vpc-k8s-ipvlan-overlay-free-kubernetes-networking-in-aws-95191201476e"
    }, 
    {
      "title": "Apple is sharing your facial wireframe with apps", 
      "url": "https://www.washingtonpost.com/news/the-switch/wp/2017/11/30/apple-is-sharing-your-face-with-apps-thats-a-new-privacy-worry/"
    }, 
    {
      "title": "Motel Living and Slowly Dying", 
      "url": "https://lareviewofbooks.org/article/motel-living-and-slowly-dying/#!"
    }
  ]
}
"""

from toapi import XPath, Item, Api

api = Api('https://news.ycombinator.com/')


class Post(Item):
    url = XPath('//a[@class="storylink"][1]/@href')
    title = XPath('//a[@class="storylink"][1]/text()')

    class Meta:
        source = XPath('//tr[@class="athing"]')
        route = '/'


api.register(Post)

api.serve()

# Visit http://127.0.0.1:5000/

"""
{
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

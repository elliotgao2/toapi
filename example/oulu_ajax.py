from toapi import Api, XPath, Item

api = Api('http://my.eudic.net/studylist', with_ajax=True)

browser = api.login('http://dict.eudic.net/account/login')
browser.find_element_by_id('input-username').send_keys('hjlarry@163.com')
browser.find_element_by_id('input-password').send_keys('123456aa')
browser.find_element_by_class_name('btn-submit').click()


class MyWords(Item):
    word = XPath('.//td[3]/a/text()')
    url = XPath('.//td[3]/a/@href')
    explanation = XPath('.//td[5]/text()')

    class Meta:
        source = XPath('//table[@id="word_table_star"]/tbody/tr')
        route = '/'


api.register(MyWords)

api.serve()

# Visit http://127.0.0.1:5000/

"""
{
  "mywords": [
    {
      "explanation": "\u611f\u52a8\u6027", 
      "url": "//dict.eudic.net/dicts/en/emotionality", 
      "word": "emotionality"
    }, 
    {
      "explanation": "\u65e0\u60c5", 
      "url": "//dict.eudic.net/dicts/en/emotionless", 
      "word": "emotionless"
    }, 
    {
      "explanation": "n. \u6fc0\u60c5\uff1b\u70ed\u60c5\uff1b\u9177\u7231\uff1b\u76db\u6012", 
      "url": "//dict.eudic.net/dicts/en/passion", 
      "word": "passion"
    }
  ]
}
"""
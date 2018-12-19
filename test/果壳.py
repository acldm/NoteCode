import requests
import json
import time
import random
from lxml import etree
from retrying import retry

class Guoke:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        self.url = "https://www.guokr.com/ask/newest/?page={0}"
        self.filename = "a.txt"
    
    @retry(stop_max_attempt_number=5)
    def get_page_tree(self, page):
        try:
            html = requests.get(self.url.format(page), headers = self.headers)
            assert html.status_code == 200
            html = etree.HTML(html.content.decode())
            time.sleep(random.randint(2, 5))
        except:
            html = None
        return html

    def getPageTreeDetail(self, tree):
        content_list = []
        if tree is None:
            return content_list
        ul = tree.xpath('//ul[@class="ask-list"]/li')
        for li in ul:
            print('---')
            item = {} 
            item["title"] = li.xpath('./div[@class="ask-list-detials"]/h2/a/text()')[0]
            item["href"] = li.xpath('./div[@class="ask-list-detials"]/h2/a/@href')[0]
            item["focus"] = li.xpath('.//p[@class="ask-focus-nums"]/span/text()')[0]      
            item["answer"] = li.xpath('.//p[@class="ask-answer-nums"]/span/text()')[0]
            item["tags"] = li.xpath('.//p[@class="tags"]/a/text()')
            item["time"] = li.xpath('.//span[@class="ask-list-time"]/text()')
            item["time"] = item["time"][0].replace("\n","")
            content_list.append(item)   
        return content_list

    def save_file(self, content_list):
        with open(self.filename, 'a', encoding='utf-8') as f:
            [f.write(json.dumps(content,ensure_ascii=False,indent=4)) for content in content_list]

    def pushPageToFile(self, page_count):
        tree = self.get_page_tree(page_count)
        content_list = self.getPageTreeDetail(tree)
        print(content_list)
        self.save_file(content_list)
        
if __name__ == "__main__":
    g = Guoke()
    for i in range(1, 10):
        print("正在爬取第{0}页".format(i))
        g.pushPageToFile(i)
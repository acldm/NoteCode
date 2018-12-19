from selenium import webdriver
import time
import json
from lxml import etree

class DouyuSpider:
    def __init__(self):
        self.url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    def get_html(self):
        li_list = self.driver.find_elements_by_xpath('//ul[@id="live-list-contentbox"]/li')
        content_list = []
        for li in li_list:
            item = {}
            item["room_name"] = li.find_element_by_xpath('.//div[@class="mes-tit"]/h3').text
            item["tag"] = li.find_element_by_xpath('.//div[@class="mes-tit"]/span').text
            item["room_img"] = li.find_element_by_xpath('.//span[@class="imgbox"]/img').get_attribute("src")
            item["room_url"] = li.find_element_by_xpath('./a[1]').get_attribute("href")
            item["user_name"] = li.find_element_by_xpath('.//div[@class="mes"]/p/span[1]').text
            item["hot"] = li.find_element_by_xpath('.//div[@class="mes"]/p/span[2]').text
            print(item)
            content_list.append(item)
        new_url = self.driver.find_elements_by_xpath('//a[@class="shark-pager-next"]')
        new_url = new_url[0] if len(new_url)>0 else None
        return content_list,new_url

    def save_data(self,content_list):
        for content in content_list:
            with open("斗鱼房间数据.txt","a",encoding="utf-8") as f:
                f.write(json.dumps(content,ensure_ascii=False,indent=4))

    def _get_html(self,html_str):
        e = etree.HTML(html_str)
        li_list = e.xpath('//ul[@id="live-list-contentbox"]/li')
        content_list = []
        for li in li_list:
            item = {}
            item["room_name"] = li.xpath('.//div[@class="mes-tit"]/h3/text()')[0].replace("\n","").strip()
            item["tag"]       = li.xpath('.//div[@class="mes-tit"]/span/text()')[0]
            item["room_img"]  = li.xpath('.//span[@class="imgbox"]/img/@src')[0]
            item["room_url"]  = li.xpath('./a[1]/@href')[0]
            item["user_name"] = li.xpath('.//div[@class="mes"]/p/span[1]/text()')[0]
            item["hot"]       = li.xpath('.//div[@class="mes"]/p/span[2]/text()')[0]
            print(item)
            content_list.append(item)

    def run(self):
        self.driver.get(self.url)
        content_list,new_url = self.get_html()
        self.save_data(content_list)
        while new_url is not None:
            new_url.click()
            time.sleep(8)
            content_list,new_url = self.get_html()
            self.save_data(content_list)
        self.driver.quit()

if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()
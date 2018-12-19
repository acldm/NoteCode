import requests
import json
import time
from lxml import etree
from retrying import retry
import threading
from queue import Queue
class QiushiSpider:
    def __init__(self):
        self.url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        # self.url_list = [self.url.format(i) for i in range(1,14)]
        self.url_queue = Queue()
        [self.url_queue.put(self.url.format(i)) for i in range(1, 6)]
        self.html_data_queue = Queue()
        self.content_list_queue = Queue()

    @retry(stop_max_attempt_number=5)
    def _get_html(self, url):
        print(url)
        time.sleep(5)
        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        assert response.status_code == 200
        return response.content.decode()

    def get_html(self):
        while True:
            url = self.url_queue.get()
            try:
                html_data = self._get_html(url)
            except:
                html_data = None
            # return html_str
            self.html_data_queue.put(html_data)
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            html_data = self.html_data_queue.get()
            e= etree.HTML(html_data)
            li_list =e.xpath("//div[contains(@id,'qiushi_tag')]")
            content_list = []
            for li in li_list:
                item = {}
                # 获取头像
                item["head_img"] = li.xpath('./div[@class="author clearfix"]/a[1]/img/@src|./div[@class="author clearfix"]/span[1]/img/@src')
                item["head_img"] = "https:" + item["head_img"][0]
                # 获取网名
                item["name"] = li.xpath( './div[@class="author clearfix"]/a[2]/h2/text()|./div[@class="author clearfix"]/span[2]/h2/text()')[0]

                # 获取性别item["sex"] = li.xpath('.//div[contains(@class,"articleGender")]/@class')
                item["sex"] = li.xpath('.//div[@class="author clearfix"]/div/@class')
                item["sex"] = item["sex"][0].split(" ")[-1].replace("Icon", "") if len(item["sex"]) > 0 else None
                # 获取年龄  item["age"] = li.xpath('.//div[contains(@class,"articleGender")]/text()')
                item["age"] = li.xpath('.//div[@class="author clearfix"]/div/text()')
                item["age"] = item["age"][0] if len(item["age"]) > 0 else None
                # 获取内容
                item["content"] = li.xpath('.//div[@class="content"]/span/text()')
                item["content"] = [i.replace("\n", "") for i in item["content"]]
                item["content"] = "".join(item["content"])
                # 获取链接
                item["url"] = li.xpath('./a[1]/@href')
                item["url"] = "https://www.qiushibaike.com" + item["url"][0]
                # 获取图片
                item["img"] = li.xpath('.//div[@class="thumb"]/a/img/@src')
                item["img"] = "http:" + item["img"][0] if len(item["img"]) > 0 else None

                # 获取好笑数量
                item["vote"] = li.xpath('.//span[@class="stats-vote"]/i/text()')[0]

                # 获取评论数量
                item["comments"] = li.xpath('.//span[@class="stats-comments"]/a/i/text()')[0]

                # 获取神评论用户#把：去掉 用replace 判断神评论用户是否为空
                item["cmt_name"] = li.xpath('.//div[@class="cmtMain"]/span[2]/text()')
                item["cmt_name"] = item["cmt_name"][0].replace(":", "") if len(item["cmt_name"]) > 0 else None
                # 获取神评论
                item["cmt_text"] = li.xpath('.//div[@class="cmtMain"]/div/text()')
                item["cmt_text"] = item["cmt_text"][0] if len(item["cmt_text"]) > 0 else None
                # 获取点赞数
                item["likenum"] = li.xpath('.//div[@class="cmtMain"]//div[@class="likenum"]/text()')
                item["likenum"] = item["likenum"][-1].replace("\n", "") if len(item["likenum"]) > 0 else None

                content_list.append(item)
            self.content_list_queue.put(content_list)
            self.html_data_queue.task_done()

    def save_data(self):
        while True:
            content_list = self.content_list_queue.get()
            for content in content_list:
                print(content)
                with open("qiushibk.txt", "a", encoding="utf-8") as f:
                    f.write(json.dumps(content, ensure_ascii=False, indent=2))

            self.content_list_queue.task_done()

    def run(self):
        thread_list = []
        for i in range(3):
            t_get_html = threading.Thread(target=self.get_html)
            thread_list.append(t_get_html)
        for i in range(2):
            t_content_list = threading.Thread(target=self.get_content_list)
            thread_list.append(t_content_list)

        t_save_data = threading.Thread(target=self.save_data)
        thread_list.append(t_save_data)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue, self.html_data_queue, self.content_list_queue]:
            q.join()


if __name__ == '__main__':
    t1 = time.time()
    guoke = QiushiSpider()
    guoke.run()
    print("程序运行了{}".format(time.time() - t1))
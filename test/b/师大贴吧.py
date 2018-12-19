import requests
import json
from lxml import etree



class TB: # 取义贴吧

    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}
        self.tb_url = "http://tieba.baidu.com/mo/q---453A87D7AA5BF60E8ED78A6378A4DA36:FG=1-sz@320_240,-1-3-0--2--wapp_1533086137983_544/"
    def get_html(self,url):
        
        response = requests.get(url,headers=self.headers)
        return response.content

    def data_cl(self,html):
        # print(html)
        e= etree.HTML(html)
        li_list = e.xpath("//div[@class='i']|//div[@class='i x']")
        content_list = []
        for li in li_list:
            item = {}
            item["title"] = li.xpath("./a/text()")[0]
            item["href"] = li.xpath("./a/@href")[0]
            item["href"] = self.tb_url + item["href"]
            item["img"] = self.img_get(item["href"],[])
            item["img"] = [requests.utils.unquote(i).split("src=")[-1] for i in item["img"]]
            content_list.append(item)

        new_url = e.xpath("//a[text()='下一页']/@href")
        new_url = self.tb_url + new_url[0] if len(new_url)>0 else None
        return content_list,new_url

    def img_get(self,img_url,total_img_list):
        img_html = self.get_html(img_url)
        img_e = etree.HTML(img_html)
        img_list = img_e.xpath("//img[@class='BDE_Image']/@src")
        total_img_list.extend(img_list)

        new_url = img_e.xpath("//a[text()='下一页']/@href")
        if len(new_url)>0 :
            new_url = self.tb_url + new_url[0]
            return self.img_get(new_url,total_img_list)
        else:
            return total_img_list

    def save_data(self,content_list):
        for content in content_list:
            print(content)
            with open("师大贴吧.txt","a",encoding="utf-8") as f:
                f.write(json.dumps(content,ensure_ascii=False,indent=2))

    def run(self):
        new_url = "http://tieba.baidu.com/mo/q---453A87D7AA5BF60E8ED78A6378A4DA36:FG=1-sz@320_240,-1-3-0--2--wapp_1533086137983_544/m?kw=福建师范大学&lp=6024"
        while new_url is not None:
            html = self.get_html(new_url)
            content_list,new_url = self.data_cl(html)
            self.save_data(content_list)

if __name__ == '__main__':
    tb = TB()
    tb.run()
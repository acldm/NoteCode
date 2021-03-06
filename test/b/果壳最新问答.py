import requests
from lxml import etree
import time
from retrying import retry
import json

class GuokeSpider:
    def __init__(self):
        '''self��ȫ�ֱ���'''
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        self.url = "https://www.guokr.com/ask/newest/?page={}"
        self.url_list = [self.url.format(i) for i in range(1,6)] #��100��ҳ�棬�ѵ�ַ������ҳ�档

    @retry(stop_max_attempt_number=5)#������δ���ִ��5��
     #�����쳣������ִ��_get_html����,
    def _get_html(self,url):#Ҫ��url����sel���������һ��url����
        '''�������󣬻�ȡ����'''
        print(url)
        time.sleep(5) #ÿ��5������ȡ��
        response = requests.get(url,headers=self.headers)
        print(response.status_code)
        assert response.status_code == 200 #�׳��쳣
         #���ԣ������׳��쳣
        return response.content.decode()

    def get_html(self,url):
        try:
            html_str = self._get_html(url)
        except:
            html_str = None

        return html_str

    def xpath_cl(self,html_str):#���html_str����
        '''�������ݣ���ȡ����Ҫ������'''
        elem = etree.HTML(html_str)
        li_list = elem.xpath('//ul[@class="ask-list"]/li')#����ڵ��ul,ask-list����ҳ����ģ�֮����li
        content_list=[]#����һ�����б���������
        content_list = []
        for li in li_list:
            #����һ���ֵ䣬����ÿһ������
            item = {} 

            #������� //�ǴӸ������⡣  ./�ǵ�ǰ
            item["title"] = li.xpath('./div[@class="ask-list-detials"]/h2/a/text()')[0]
            
            #��������
            item["href"] = li.xpath('./div[@class="ask-list-detials"]/h2/a/@href')[0]
            
            #�����ע��
            item["focus"] = li.xpath('.//p[@class="ask-focus-nums"]/span/text()')[0]
     
             #����ش���           
            item["answer"] = li.xpath('.//p[@class="ask-answer-nums"]/span/text()')[0]

            #�����ǩ
            item["tags"] = li.xpath('.//p[@class="tags"]/a/text()')

            #�����ڱ߱��ϵ�ʱ��
            item["time"] = li.xpath('.//span[@class="ask-list-time"]/text()')
            #[0]��ת�����ַ���
            item["time"] = item["time"][0].replace("\n","")
            
            content_list.append(item)#���ֵ�Ž��б�����

        return content_list#�������ս��


    '''��������'''
    def sava_date(self,content_list):#content_list���б�
        for content in content_list:
            with open("GuokeNew.txt","a",encoding="utf-8") as f:
                f.write(json.dumps(content,ensure_ascii=False,indent=4))


    def run(self):
    	  # 1.����url����
        for url in self.url_list:
          # 2.�õ���Ӧ����ȡ����
            html_str = self.get_html(url)#Ҫ�������url���ݸ����������return�ᱻhtml_str����
            # 3.xpath�����ݽ��д���
            if html_str is not None:
                content_list = self.xpath_cl(html_str)#�ж�html_str�Ƿ�Ϊ��
                # 4.��������
                self.sava_date(content_list)#����
            else:
                self.url_list.append(url)

if __name__ == '__main__':
    t1 = time.time()
    guoke = GuokeSpider()
    guoke.run()
    print("����������{}��".format(time.time()-t1))
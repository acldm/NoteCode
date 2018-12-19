import requests
import json
#OOP之所以是OOP,是实实在在解决问题而发明的。不是直接将过程式的东西扔到类里面就可以了,那不叫OOP,那叫皇帝的新装
#这种小爬虫，根本不用继承,多态,只要善于利用封装,代码就能清晰很多
class FY:
    def __init__(self):
        #声明所有需要的类级资源
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Mobile Safari/537.36"}
        self.trans_url = 'https://fanyi.baidu.com/basetrans'
        self.detect_url = 'https://fanyi.baidu.com/langdetect'

    #翻译核心方法，传入需要翻译的词,返回结果
    def trans(self, keyword):
        data = self.detect(keyword)
        return self.json_post(self.trans_url, data)["trans"][0]["dst"]
    
    #判断语言类别
    def detect(self, keyword):
        data = {
            "query": keyword
        }
        res = self.json_post(self.detect_url, data)
        data['from'] = res["lan"]
        data["to"] = "en" if res["lan"] == "zh" else "zh"
        return data
    
    #既然该爬虫全部都是使用json格式的数据，为什么不一开始HTTP请求后就直接返回JSON呢？
    def json_post(self, url, data):
        res = requests.post(url, headers = self.headers, data = data)
        return json.loads(res.content.decode())

if __name__ == "__main__":
    ins = FY()
    #输入=>处理=>输出应该是分离的,类应该是可复用的
    query_word = input("请输入需要翻译的内容:")
    answer = ins.trans(query_word)
    print(answer)
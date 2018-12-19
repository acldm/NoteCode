import requests
import json

class FY:
    def __init__(self):
        self.headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
    #1.��������
    def send_post(self,url,data):
        response=requests.post(url,headers=self.headers,data=data)
        return response.content.decode()

    #2./��������
    def set_data(self,query_string):
        lan_url="https://fanyi.baidu.com/langdetect"  #�ж����Ļ���Ӣ�� 
        lan_data={
            "query" : query_string
        } 
        
        lan_dict = self.send_post(lan_url,lan_data)
        lan=json.loads(lan_dict)["lan"]
        
        data={
            "from":lan,
            "to":"en" if lan == "zh" else "zh", 
            "query":query_string
        }
        return data

    #3.�������ݣ�������
    def print_data(self,trans_data):
        ret=json.loads(trans_data)
        print(ret["trans"][0]["dst"])


    #4.��������
    def run(self):
        query_string = input("��������Ҫ��������֣�")
        url = "https://fanyi.baidu.com/basetrans"
        data= self.set_data(query_string)
        ret = self.send_post(url,data)
        self.print_data(ret)

if __name__ == '__main__':
    fy = FY()
    fy.run()

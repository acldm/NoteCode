import requests
import json
import re
# 新添加的类 函数 都可以改
class MUSIC:# 百度音乐 以MUSIC命名 
    
    def __init__(self): # 构造函数
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        # 有headers的地方都要写成 self.headers呀呀！！
        

    def send(self):  # 发送请求函数 send命名
        Kw={
            "key":"林俊杰"
        }
        url="http://music.taihe.com/search"
        response=requests.get(url,headers=self.headers,params=Kw)

        song_id=re.findall('data-songdata=\'{ "id": "(\d+)" }\'',response.content.decode())

        song_data={
            "songIds":",".join(song_id),
            "hq": "0",
            "type": "m4a,mp3",
            "rate":"",
            "pt": "0",
            "flag": "-1",
            "s2p": "-1",
            "prerate": "-1",
            "bwt": "-1",
            "dur": "-1",
            "bat":"-1",
            "bp": "-1",
            "pos":"-1",
            "auto": "-1"
        }

        return song_data # 返回song—_data值

    def save(self,song_url,song_data): # 保存函数 save 命名
        new_response=requests.post(song_url,data=song_data,headers=self.headers)
        ret=json.loads(new_response.content.decode())
        ret=ret["data"]["songList"]

        for i in ret:
            songname=i["songName"]
            songlink=i["songLink"]
            song_response=requests.get(songlink,headers=self.headers)
            with open("%s.mp3"%songname,"wb")as f:
                f.write(song_response.content)

    def run(self): # run开始运行函数
        song_url="http://play.taihe.com/data/music/songlink"
        song_data = self.send()
        self.save(song_url,song_data)

if __name__ == "__main__":
    music = MUSIC()
    music.run()
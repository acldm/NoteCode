import requests
import json
import re
class Music:
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        }
        self.search_url = "http://music.taihe.com/search"
        self.song_url = "http://play.taihe.com/data/music/songlink"
    
    def search(self, key):
        r = requests.get(self.search_url, headers = self.headers, params = {'key': key})
        ls = re.findall('data-songdata=\'{ "id": "(\d+)" }\'', r.content.decode())

        data = {
            "songIds":','.join(ls),
            "hq": 0,
            "type": "m4a,mp3",
            "rate":'', 
            "pt": 0,
            "flag": -1,
            "s2p": -1,
            "prerate": -1,
            "bwt": -1,
            "dur": -1,
            "bat": -1,
            "bp": -1,
            "pos": -1,
            "auto": -1
        }
        new_response = requests.post(self.song_url,data=data,headers=self.headers)
        ret=json.loads(new_response.content.decode())

        return ret["data"]["songList"]

    def downloads(self, song_list):
        for song in song_list:
            songname, songlink = song["songName"], song["songLink"]
            song_response=requests.get(songlink,headers=self.headers)
            with open("%s.mp3" % songname,"wb")as f:
                f.write(song_response.content)

    def download_songs(self, keyword):
        song_list = self.search(keyword)
        self.downloads(song_list)

if __name__ == "__main__":
    m = Music()
    m.download_songs("rose")
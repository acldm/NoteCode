import requests
import re
import json

class Kr:
    def __init__(self):
        self.url = "https://36kr.com/newsflashes"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

    def run(self):
        r = requests.get(self.url, headers = self.headers)
        # 正则表达式
        s = re.findall("<script>var props=(.*),locationnal", r.content.decode())[0]
        print(s)
        js = json.loads(s)
        self.save("a.txt", js)

    def save(self, filename, js):
        with open(filename, 'w', encoding='utf-8') as f:
            for c in js["newsflashList|newsflash"]:
                f.write(c['template_info']['template_title'])
                f.write('\n')

if __name__ == "__main__":
    Kr().run()
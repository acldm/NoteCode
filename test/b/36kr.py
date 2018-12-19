import requests
import re
import json

class KR: # 36kr 以KR为类名
	def __init__(self):
		self.url="https://36kr.com/newsflashes"
		#url = "http://36kr.com/"

		self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
	def run(self):	# run函数
		response=requests.get(self.url,headers=self.headers)
		json_data=re.findall("<script>var props=(.*?)</script> ",response.content.decode())

		ret=re.sub(",locationnal=.*","",json_data[0])

		new_ret=json.loads(ret)
		self.save(new_ret) # 调用保存函数 可以不写
		print(ret)

	def save(self,new_ret): # 保存函数 可以不写
		#for i in new_ret["feedPostsLatest|post"]:
		for i in new_ret["newsflashList|newsflash"]:
			with open("36kr_new7×24.txt","a",encoding="utf-8")as f:
				f.write(i["title"])
				f.write("\n")
				f.write("-"*100)
				f.write("\n")
				f.write(i["description"])
				f.write("\n")
				f.write("="*50)
				f.write("\n")

		#		f.write(i["id"])
		# 		f.write("\n")
		# 		f.write(i["title"])
		# 		f.write("\n")
		# 		f.write(i["summary"])
		# 		f.write("\n")
		# 		f.write("*"*100)
		# 		f.write("\n")
if __name__ == "__main__":
	kr = KR()
	kr.run()

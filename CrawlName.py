from fake_useragent import UserAgent
import requests
from pymongo import MongoClient
import time
import json
ua = UserAgent()
errorlinks=[]
class NongGuanJia():
    def __init__(self):
        self.headers = {"User-Agent": ''}
    def getrequest(self, url):
        # 使用随机的user-agent
        self.headers["User-Agent"] = ua.random
        try:
            r = requests.get(url, headers=self.headers, timeout=8)
            #print("requested from:" + url)
            return r
        except requests.exceptions.ReadTimeout:
            print("requests.exceptions.ReadTimeout")
            time.sleep(8)
            r = self.getrequest(url)
            return r
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
            time.sleep(8)
            r = self.getrequest(url)
            return r
        except BaseException:
            print("error")
            time.sleep(8)
            r = self.getrequest(url)
            return r

    def decodejson(self, r, url):
        i = 0
        try:
            data = r.json()
        except json.decoder.JSONDecodeError:
            i = i + 1
            if(i < 10):  # 允许10次JSONDecodeError
                time.sleep(3)
                self.decodejson(r, url)
                return data
        except Exception as e:
            print("Error:", e)
            r = self.getrequest(url)
            data = r.json()
            return data
        return data
    def updateCropName(self,qid):
        url='http://ngjv4.laodao.so/ASHX/bbs_card.ashx?action=replylist&version=pc&ID='+qid+'&pagSize=20&pagindex=1'
        r=self.getrequest(url)
        data=self.decodejson(r,url)
        rcode = data["code"]
        if (rcode == 200):
            return data['message']['Name']
        else:
            print('error link:'+url)
            errorlinks.append(url)
            import json
            errorlinkstocrawl = open("./errorlinkstocrawl.json", 'w')
            json.dump(
                errorlinks,
                errorlinkstocrawl,
                indent=4,
                sort_keys=False,
                ensure_ascii=False)
            errorlinkstocrawl.close()
crawler=NongGuanJia()
client = MongoClient()
db = client['NongGuanJia']
pcoll=db['NongGuanJiaByProblem']
cursor = pcoll.find()
for document in cursor:
    try:
        if document['Name']!=None:
            pass
    except KeyError:
        cropname=crawler.updateCropName(str(document['qid']))
        pcoll.update_one(
            {"_id":document["_id"]},
            {
                "$set": {
                    "Name": cropname
                }
            }

        )
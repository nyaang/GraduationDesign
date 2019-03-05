from fake_useragent import UserAgent
import requests
import pymongo
import threading
import time
import json
problemids = json.load(open("problemids.json", 'r'))
ua = UserAgent()


class NongGuanJia(threading.Thread):
    def __init__(self, ownproblemids):
        threading.Thread.__init__(self)
        self.problemids = ownproblemids

    def run(self):
        for problemid in self.problemids:
            self.headers = {"User-Agent": ''}
            self.getfollow(problemid)

    def getrequest(self, url):
        # 使用随机的user-agent
        self.headers["User-Agent"] = ua.random
        try:
            r = requests.get(url, headers=self.headers, timeout=8)
            print("requested from:" + url)
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

    def getfollow(self, problemid):
        url = 'http://ngjv4.laodao.so/ASHX/bbs_card.ashx?action=replylist&version=pc&ID=%s&pagSize=20&pagindex=1' % (
            problemid)
        r = self.getrequest(url)
        data = self.decodejson(r, url)
        datas = data["datas"]
        qreply = []
        if(len(datas) == 0):
            problemids.remove(problemid)
            self.updateuserids()
        else:
            for j in range(0, len(datas)):
                content = datas[j]["contents"]  # 回复的内容
                ruid = datas[j]["UserID"]
                # 值皆为2，为3时是提问者显示其他
                ridentities = datas[j]['identities']
                rtime = datas[j]["CreateTime"]  # 回复时间
                pro = datas[j]['Province']
                city = datas[j]['City']
                keyword = datas[j]['keyword']
                zan = datas[j]["zan"]  # 赞
                cai = datas[j]["cai"]  # 踩
                qreply.append({"content": content,
                               "ruid": ruid,
                               "ridentities": ridentities,
                               "province": pro,
                               "city": city,
                               "keyword": keyword,
                               "time": rtime,
                               "zan": zan,
                               "cai": cai})
            client = pymongo.MongoClient('127.0.0.1:27017')
            db = client['NongGuanJia']
            db['NongGuanJiaByProblem'].insert_one({
                "id": problemid,
                "reply": qreply
            })
            problemids.remove(problemid)

            self.updateuserids()

    def updateuserids(self):
        userfile = open('problemidsnew.json', 'w')
        json.dump(
            problemids,
            userfile,
            indent=4,
            sort_keys=False,
            ensure_ascii=False)
        userfile.close()


def start(threadnum):
    linksqueue = []
    links_len = len(problemids)
    split_num = links_len // threadnum
    i = 1
    while (i < threadnum):
        linki = problemids[split_num * (i - 1):split_num * i]
        linksqueue.append(NongGuanJia(linki))
        i = i + 1
    linkend = problemids[split_num * (i - 1):links_len]
    linksqueue.append(NongGuanJia(linkend))
    i = 0
    while (i < threadnum):
        linksqueue[i].start()
        i = i + 1


start(1)

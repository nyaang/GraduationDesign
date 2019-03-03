import requests,pymongo,threading,time,json,re,random,math
userids = json.load(open("userids.json",'r'))
class NongGuanJia(threading.Thread):
    def __init__(self, userids):
        threading.Thread.__init__(self)
        self.userids = userids
        self.knum=0
    def run(self):
        for userid in self.userids:
            self.userid = userid
            self.getfollow(self.userid)
    def getrequest(self, url):
        #proxie = json.load(open("proxies.json", 'r'))
        try:
            #proxy = random.choice(proxie)
            #r = requests.get(url, timeout=10, proxies=proxy)
            r = requests.get(url, timeout=3)
            print("requested from:" + url)
            return r
        except requests.exceptions.ReadTimeout:
            print("requests.exceptions.ReadTimeout")
            time.sleep(1)
            r = self.getrequest(url)
            return r
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
            time.sleep(1)
            r = self.getrequest(url)
            return r
        except:
            print("error")
            time.sleep(1)
            r = self.getrequest(url)
            return r
    def decodejson(self,r,url):
        i=0
        try:
          data = r.json()
        except json.decoder.JSONDecodeError:
            i=i+1
            if(i<10):   #允许10次JSONDecodeError
              time.sleep(3)
              self.decodejson(r, url)
              return data
        except Exception as e:
            print("Error:",e)
            r = self.getrequest(url)
            data = r.json()
            return data
        return data

    def getfollow(self,userid):
        nowtime = '2019-03-01T00:00:00' #最新的抓取时间
        self.rcount = 0 #回复数
        self.qcount = 0 #问题数
        self.User = []
        self.Reply = []
        self.Question = []
        crop = set()
        while (nowtime != 'none'):
          print(nowtime)
          url = 'http://ngjv4.laodao.so//ashx/news/sys_FriendNews.ashx?action=find4user&UserID=%s&lasttime=%s&pckey=&version=pc' % (self.userid,nowtime)
          r = self.getrequest(url)
          data =self.decodejson(r,url)
          datas = data["datas"]
          code=data["code"] #响应码
          print(code)
          if (len(datas) == 20):
                nowtime = datas[-1]["UpdateDate"]
          else:
                nowtime = 'none'    #当前页以为最末页
          if (code ==200 and len(datas)>0):
            print("ok")
            for i in range(0, len(datas)):
                qid = datas[i]['CardID']    #问题Id
                cropid = datas[i]["CropID"] #植物Id
                abs = datas[i]['abs']   #问题文字摘要
                aorq = datas[i]['type'] #值为0，表示提问；值为3，表示回答
                self.identities = datas[i]['identities']
                self.pro = datas[i]['Province']
                self.city=datas[i]['City']
                recount = datas[i]['ReplyCount'] #回答数
                time = datas[i]["UpdateDate"]

                if (aorq == 3): #抓回答
                    self.rcount += 1
                    self.Reply.append({"qid": qid,
                                       "cropid":cropid,
                                  "abs": abs,
                                  "recount": recount,
                                  "time": time})
                    crop.add(cropid)

                else: #抓问题
                    print(qid)
                    self.qcount += 1
                    if (int(recount) <= 20):
                        rurl = 'http://ngjv4.laodao.so/ASHX/bbs_card.ashx?action=replylist&version=pc&ID=%s&pagSize=20&pagindex=1' % (
                            qid)
                        rr = self.getrequest(rurl)
                        rdata = self.decodejson(rr,rurl)
                        rcode = rdata["code"]
                        if (rcode == 200):
                           rdatas = rdata["datas"]
                           qreply = []
                           for j in range(0, len(rdatas)):
                            content = rdatas[j]["contents"] #回复的内容
                            ruid = rdatas[j]["UserID"]
                            ridentities = rdatas[j]['identities'] #值皆为2，为3时是提问者显示其他
                            rtime = rdatas[j]["CreateTime"] #回复时间
                            pro = rdatas[j]['Province']
                            city= rdatas[j]['City']
                            zan = rdatas[j]["zan"] #赞
                            cai = rdatas[j]["cai"] #踩
                            qreply.append({"content": content,
                                           "ruid": ruid,
                                           "ridentities": ridentities,
                                           "province": pro,
                                           "city":city,
                                           "time": rtime,
                                           "zan": zan,
                                           "cai": cai})
                        else:
                            qreply=[]
                            print("问题网页响应码不为200，为"+str(rcode))
                    else:
                        k = int(recount) // 20 + 1  #不必要的循环，20不是每页加载的最大回复数，最多可加载的回复数待求证，TODO
                        print("recount:"+str(recount))
                        for m in range(1, k+1):
                            rurl = 'http://ngjv4.laodao.so/ASHX/bbs_card.ashx?action=replylist&version=pc&ID=%s&pagSize=20&pagindex=%s' % (
                                qid, m)
                            rr = self.getrequest(rurl)
                            rdata = self.decodejson(rr,rurl)
                            rcode = rdata["code"]

                            if (rcode == 200):
                             rdatas = rdata["datas"]
                             qreply = []

                             for j in range(0, len(rdatas)):
                                content = rdatas[j]["contents"]
                                ruid = rdatas[j]["UserID"]
                                ridentities = rdatas[j]['identities']
                                rtime = rdatas[j]["CreateTime"]
                                pro = rdatas[j]['Province']
                                zan = rdatas[j]["zan"]
                                cai = rdatas[j]["cai"]
                                qreply.append({"content": content,
                                               "ruid": ruid,
                                               "ridentities": ridentities,
                                               "province": pro,
                                               "time": rtime,
                                               "zan": zan,
                                               "cai": cai})
                            else:
                                qreply=[]
                                print("问题网页响应码不为200，为" + str(rcode))
                    self.Question.append({"qid": qid,
                                          "cropid":cropid,
                                     "question": abs,
                                     "recount": recount,
                                     "time": time,
                                     "reply": qreply})

        if(len(datas)>0):   #筛去没有任何动态（问题或回答）的用户
           self.User.append({"uid": self.userid,
                    "identities": self.identities,
                    "rcount": self.rcount,
                    "qcount": self.qcount,
                    "province": self.pro,
                    "city":self.city,
                    "crops": list(crop)
            })

        if(len(self.User)>0):
          client = pymongo.MongoClient('127.0.0.1:27017')
          db = client['Nongguanjia']
          db['nongguanjianew'].insert_one(
            {"User": self.User,
            "Question":self.Question,
            "Reply":self.Reply})

        userids.remove(self.userid)
        self.updateuserids()

    def updateuserids(self):
      userfile = open('usersnew.json', 'w')
      json.dump(userids, userfile, indent=4, sort_keys=False, ensure_ascii=False)
      userfile.close()

def start(threadnum):
    linksqueue = []
    links_len = len(userids)
    split_num = links_len // threadnum
    i = 1
    while (i < threadnum):
        linki = userids[split_num * (i - 1):split_num * i]
        linksqueue.append(NongGuanJia(linki))
        i = i + 1
    linkend = userids[split_num * (i - 1):links_len]
    linksqueue.append(NongGuanJia(linkend))
    i = 0
    while (i < threadnum):
        linksqueue[i].start()
        i = i + 1
start(3)




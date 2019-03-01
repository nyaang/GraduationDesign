import requests, re,  json, random, pymongo, threading,math,time,json
# from lxml import etree
# from time import localtime
userids = json.load(open("userids.json", 'r'))



class wbrelation(threading.Thread):
    def __init__(self, userids):
        threading.Thread.__init__(self)
        self.userids = userids
        self.knum=0

    def run(self):
        for userid in self.userids:
            self.userid = userid
            self.getfollow(self.userid)



    def getrequest(self, url):
       # proxie = json.load(open("proxies.json", 'r'))

        try:

          #  proxy = random.choice(proxie)
           # r = requests.get(url, timeout=10, proxies=proxy)
            r = requests.get(url, timeout=10)
            print("requested from:" + url)
            #print (r)
            return r
        except requests.exceptions.ReadTimeout:
            print("requests.exceptions.ReadTimeout")
            r = self.getrequest(url)
            return r
        except requests.exceptions.ConnectionError:
            r = self.getrequest(url)
            return r
        except :
            r = self.getrequest(url)
            return r




    def decodejson( self,r,url):
        i=0
        try:

          data = r.json()

        except json.decoder.JSONDecodeError:
            i=i+1
            if(i<10):


              time.sleep(3)
              self.decodejson( r, url)
              return data


        except Exception as  e:
            print("e :")
            print (e)
            r = self.getrequest(url)
            data = r.json()
            return data
        return data


# 48\

    def getfollow(self,userid):

        nowtime = '2018-09-10T00:00:00'
        self.rcount = 0
        self.qcount = 0
        self.User = []
        self.Reply = []
        self.Question = []
        crop = set()
        while (nowtime != 'none'):
          print(nowtime)
          url = 'http://ngjv4.laodao.so//ashx/news/sys_FriendNews.ashx?action=find4user&UserID=%s&lasttime=%s&pckey=&version=pc' % (self.userid,nowtime)
          r = self.getrequest(url)
          data =self.decodejson(r,url)
          data1 = data["datas"]
          code=data["code"]
          print(code)
          if (len(data1) == 20):
                nowtime = data1[-1]["UpdateDate"]
          else:
                nowtime = 'none'
          if (code ==200 and len(data1)>0):
            print("ok")
            for i in range(0, len(data1)):
                qid = data1[i]['CardID']
                cropid = data1[i]["CropID"]
                self.uid = data1[i]['UserID']
                abs = data1[i]['abs']
                aorq = data1[i]['type']
                self.identities = data1[i]['identities']
                self.pro = data1[i]['Province']
                recount = data1[i]['ReplyCount']
                time = data1[i]["UpdateDate"]

                if (aorq == 3):
                    self.rcount += 1
                    self.Reply.append({"qid": qid,
                                       "cropid":cropid,
                                  "abs": abs,
                                  "recount": recount,
                                  "time": time})
                    crop.add(cropid)

                else:
                    print(qid)
                    self.qcount += 1
                    if (int(recount) <= 20):
                        rurl = 'http://ngjv4.laodao.so/ASHX/bbs_card.ashx?action=replylist&version=pc&ID=%s&pagSize=20&pagindex=1' % (
                            qid)
                        rr = self.getrequest(rurl)
                        rdata = self.decodejson(rr,rurl)
                        rcode = rdata["code"]

                        if (rcode == 200):
                           rdata1 = rdata["datas"]

                           qreply = []

                           for j in range(0, len(rdata1)):
                            content = rdata1[j]["contents"]
                            ruid = rdata1[j]["UserID"]

                            ridentities = rdata1[j]['identities']

                            rtime = rdata1[j]["CreateTime"]
                            pro = rdata1[j]['Province']
                            zan = rdata1[j]["zan"]
                            cai = rdata1[j]["cai"]
                            qreply.append({"content": content,
                                           "ruid": ruid,
                                           "ridentities": ridentities,
                                           "province": pro,
                                           "time": rtime,
                                           "zan": zan,
                                           "cai": cai})
                        else:
                            qreply=[]
                    else:

                        k = int(recount) // 20 + 1
                        for m in range(1, k+1):
                            rurl = 'http://ngjv4.laodao.so/ASHX/bbs_card.ashx?action=replylist&version=pc&ID=%s&pagSize=20&pagindex=%s' % (
                                qid, m)
                            rr = self.getrequest(rurl)
                            rdata = self.decodejson(rr,rurl)
                            rcode = rdata["code"]

                            if (rcode == 200):
                             rdata1 = rdata["datas"]

                             qreply = []

                             for j in range(0, len(rdata1)):
                                content = rdata1[j]["contents"]
                                ruid = rdata1[j]["UserID"]

                                ridentities = rdata1[j]['identities']

                                rtime = rdata1[j]["CreateTime"]
                                pro = rdata1[j]['Province']
                                zan = rdata1[j]["zan"]
                                cai = rdata1[j]["cai"]
                                qreply.append({"content": content,
                                               "ruid": ruid,
                                               "ridentities": ridentities,
                                               "province": pro,
                                               "time": rtime,
                                               "zan": zan,
                                               "cai": cai})
                            else:
                                qreply=[]
                    self.Question.append({"qid": qid,
                                          "cropid":cropid,
                                     "question": abs,
                                     "recount": recount,
                                     "time": time,
                                     "reply": qreply})

        if(len(data1)>0):
           self.User.append({"uid": self.userid,
                    "identities": self.identities,
                     "rcount": self.rcount,
                     "qcount": self.qcount,

                   "province": self.pro,
                   "crops": list(crop)
            })

        if(len(self.User)>0):
          client = pymongo.MongoClient('127.0.0.1:27017')
          db = client['Nongguanjia']
          db['nongguanjianew'].insert(
          {"User": self.User,
                            "Question":self.Question,
                           "Reply":self.Reply})

        userids.remove(self.userid)
        self.updateuserids(self.userid)



    def updateuserids(self,userid):
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
        linksqueue.append(wbrelation(linki))
        i = i + 1
    linkend = userids[split_num * (i - 1):links_len]
    linksqueue.append(wbrelation(linkend))
    i = 0
    while (i < threadnum):
        linksqueue[i].start()
        i = i + 1
start(3)




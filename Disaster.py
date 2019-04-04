from fake_useragent import UserAgent
import requests
import pymongo
import time
import json
ua = UserAgent()
errorlinks = []


class disater():
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

    def updaterrorlinks(self, url):
        errorlinks.append(url)
        errorlinksfile = open("./errorlinks.json", 'w')
        json.dump(
            errorlinks,
            errorlinksfile,
            indent=4,
            sort_keys=False,
            ensure_ascii=False)
        errorlinksfile.close()

    def decodejson(self, r, url):
        try:
            data = r.json()
        except json.decoder.JSONDecodeError:
            if r.status_code == 500:
                print('error 500')
                self.updaterrorlinks(url)
                return 'error 500'
        return data

    def crawlzbbh(self, urlid):
        self.drugsurl = "http://ngjv4.laodao.so/ashx/fm_DiseaseSolution.ashx?action=listapp&pagSize=500&pagIndex=1&SolutionSource=0&DiseaseID=" + urlid
        self.url = 'http://ngjv4.laodao.so/api/pub/cropdisease.ashx?action=info&disid=' + urlid
        self.headers = {"User-Agent": ''}
        disater_r = self.getrequest(self.url)
        disater_data = self.decodejson(disater_r, self.url)
        if disater_data == 'error 500':
            return
        drug_r = self.getrequest(self.drugsurl)
        drug_data = self.decodejson(drug_r, self.drugsurl)
        if disater_data["code"] == 200:
            datas = disater_data["datas"]
            self.CropID = datas["CropID"]
            self.Name = datas["Name"]
        if len(drug_data["datas"]):
            self.drugs = drug_data["datas"][0]["Drug"]
            client = pymongo.MongoClient('127.0.0.1:27017')
            db = client['NongGuanJia']
            db['NongGuanJiazbbh'].insert_one(
                {"id": urlid,
                 "Name": self.Name,
                 "CropID": self.CropID,
                 "Url": self.url,
                 "Drug": self.drugs,
                 "Drugurl": self.drugsurl
                 })

    def crawlynzz(self, url):
        self.headers = {"User-Agent": ''}
        r = self.getrequest(url)
        data = self.decodejson(r, url)
        keyword = data["datas"]["keyWord"]
        reasons = data["datas"]["reasons"]
        solution = data["datas"]["solution"]
        CropClassID = data["datas"]["CropClassID"]
        CropID = data["datas"]["CropID"]
        client = pymongo.MongoClient('127.0.0.1:27017')
        db = client['NongGuanJia']
        db['NongGuanJiaynzz'].insert_one(
            {"url": url,
             "keyword": keyword,
             "CropClassID": CropClassID,
             "CropID": CropID,
             "reasons": reasons,
             "solution": solution
             })


def zbbhstart():
    d = disater()
    links = json.load(open("./zbbhfile.json", 'r'))
    for link in links:
        d.crawlzbbh(link['link'][66:])
    # 8421麦叶峰未解决
    # 8361大螟未解决


def ynzzstart():
    d = disater()
    links = json.load(open("./ynzzfile.json", 'r'))
    for link in links:
        d.crawlynzz(link["link"])

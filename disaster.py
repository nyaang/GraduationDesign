from fake_useragent import UserAgent
import requests
import pymongo
import time
import json
ua = UserAgent()
DrugUrls="http://ngjv4.laodao.so/ashx/fm_DiseaseSolution.ashx?action=listapp&pagSize=500&pagIndex=1&SolutionSource=0&DiseaseID=2000"
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
    def run(self,urlnum):
        # url="http://ngjv4.laodao.so/ashx/fm_DiseaseSolution.ashx?action=listapp&pagSize=500&pagIndex=1&SolutionSource=0&DiseaseID="+str(urlnum)
        # self.headers = {"User-Agent": ''}
        # r=self.getrequest(url)
        # data=self.decodejson(r,url)
        # #print(len(data["datas"]))
        # if len(data["datas"]):
        #     #self.drugs=data["datas"][0]["Drug"]
        #     self.drugsurl=url
        #     self.url='http://ngjv4.laodao.so/api/pub/cropdisease.ashx?action=info&disid='+str(urlnum)
        #     disater_r=self.getrequest(self.url)
        #     disater_data=self.decodejson(disater_r,self.url)
        #     datas=disater_data["datas"]
        #     self.CropID=datas["CropID"]
        #     self.Name=datas["Name"]
        #     client = pymongo.MongoClient('127.0.0.1:27017')
        #     db = client['NongGuanJia']
        #     db['Disaster'].insert_one(
        #         {"id":urlnum,
        #          "Name": self.Name,
        #          "Url": self.url,
        #          #"Drug": self.drugs,
        #          "Drugurl":self.drugsurl,
        #          "CropID":self.CropID})
        self.headers = {"User-Agent": ''}
        #http://ngjv4.laodao.so/ashx/dd/dd_DifficultDis.ashx?action=info&ID=297
        #http://ngjv4.laodao.so/ashx/fm_DiseaseSolution.ashx?action=listapp&pagSize=500&pagIndex=1&SolutionSource=0&DiseaseID=2977
        self.url='http://ngjv4.laodao.so/api/pub/cropdisease.ashx?action=info&disid='+str(urlnum)
        disater_r=self.getrequest(self.url)
        disater_data=self.decodejson(disater_r,self.url)
        if disater_data["code"]==200:
            datas=disater_data["datas"]
            self.CropID=datas["CropID"]
            self.Name=datas["Name"]
            client = pymongo.MongoClient('127.0.0.1:27017')
            db = client['NongGuanJia']
            db['NongGuanJiaByDisaster'].insert_one(
                {"id":urlnum,
                 "Name": self.Name,
                 "Url": self.url,
                 "CropID":self.CropID})
d=disater()
# for i in range(1,2225):
#     d.run(i)
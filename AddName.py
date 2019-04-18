from pymongo import MongoClient
croplistOrigin=['', '栽培', '番茄', '甜瓜', '花生', '香蕉', '桃树', '草莓', '粮油', '水稻', '葡萄', '施肥', '柑橘', '西瓜', '意见反馈', '根菜', '马铃薯', '梨树', '水果', '李子', '樱桃', '黄瓜', '棉麻', '叶菜', '苹果', '芒果', '火龙果', '瓜菜', '植保', '辣椒']
removeedCrop=['','栽培','粮油','施肥','意见反馈','水果','植保']
croplist=['番茄', '甜瓜', '花生', '香蕉', '桃树', '草莓', '水稻', '葡萄', '柑橘', '西瓜', '根菜', '马铃薯', '梨树', '李子', '樱桃', '黄瓜', '棉麻', '叶菜', '苹果', '芒果', '火龙果', '瓜菜', '辣椒']

client = MongoClient()
db = client['NongGuanJia']
pcoll=db['NongGuanJiaByProblem']
cursor=pcoll.find()
foundlist=[]
for document in cursor:
    if document['Name'] in removeedCrop:
        question=document['question']

        content = question
        for reply in document['reply']:
            content = content + ' ' + reply['content']
        namefind = ''

        for crop in croplist:
            if question.find(crop)!=-1:
                namefind = crop
                pcoll.update_one(
                    {"_id": document["_id"]},
                    {
                        "$set": {
                            "NameFind": namefind
                        }
                    }

                )
                foundlist.append(document['qid'])
                print(crop+str(document['qid']))
                break
        if namefind=='':
            maxvalue=0
            for crop in croplist:
                if content.count(crop) > maxvalue:
                    maxvalue = content.count(crop)
                    namefind = crop
            if maxvalue > 0:
                pcoll.update_one(
                    {"_id": document["_id"]},
                    {
                        "$set": {
                            "NameFind": namefind
                        }
                    }

                )
                foundlist.append(document['qid'])
                print(namefind + str(document['qid']))
        # if namefind=='':
        #     #print('None'+ str(document['qid']))
        #     pass
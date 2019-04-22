from pymongo import MongoClient
croplistOrigin=['', '栽培', '番茄', '甜瓜', '花生', '香蕉', '桃树', '草莓', '粮油', '水稻', '葡萄', '施肥', '柑橘', '西瓜', '意见反馈', '根菜', '马铃薯', '梨树', '水果', '李子', '樱桃', '黄瓜', '棉麻', '叶菜', '苹果', '芒果', '火龙果', '瓜菜', '植保', '辣椒']
removeedCrop=['','栽培','粮油','施肥','意见反馈','水果','植保']
croplist=['番茄', '甜瓜', '花生', '香蕉', '桃树', '草莓', '水稻', '葡萄', '柑橘', '西瓜', '根菜', '马铃薯', '梨树', '李子', '樱桃', '黄瓜', '棉麻', '叶菜', '苹果', '芒果', '火龙果', '瓜菜', '辣椒']

client = MongoClient()
db = client['NongGuanJia']
pcoll=db['NongGuanJiaByProblem']
cursor=pcoll.find()
foundlist=[]
temp=''
def addname():
    for document in cursor:
        try:
            temp=document['NameFind']
        except KeyError:
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
def countcrop():
    # notdetailcrop = 0
    # detailcrop = 0
    # for document in cursor:
    #     if document['Name'] in croplist:
    #         detailcrop += 1
    #     else:
    #         notdetailcrop += 1
    # print(detailcrop, notdetailcrop)
    # notdetailcrop = 0
    # detailcrop = 0
    # cursor = pcoll.find()
    # for document in cursor:
    #     try:
    #         if document['NameFind'] != None:
    #             detailcrop += 1
    #     except KeyError:
    #         if document['Name'] in croplist:
    #             detailcrop += 1
    #         else:
    #             notdetailcrop += 1
    # print(detailcrop, notdetailcrop)
    keywordandnameproblem=0
    keywordproblem=0
    keywordplist=[]
    for document in cursor:
        try:
            if document['NameFind']!=None and document['keywordNum']>0:
                keywordandnameproblem+=1
                keywordproblem+=1
        except KeyError:
            if document['Name'] in croplist and document['keywordNum']>0:
                keywordandnameproblem += 1
                keywordproblem += 1
            elif document['keywordNum']>0:
                keywordproblem += 1
                keywordplist.append(document['Name'])
    import copy
    keywordplistcopy=copy.deepcopy(keywordplist)
    keywordplistcopy=set(list(keywordplistcopy))
    for p in keywordplistcopy:
        print(p+str(keywordplist.count(p)))
    print(keywordandnameproblem,keywordproblem)
countcrop()
from pymongo import MongoClient
client = MongoClient()
db = client['NongGuanJia']
coll=db['NongGuanJiaByUser']
def quchong():  #去重
    newcoll=db['NongGuanJiaByUserNew']
    cursor=coll.find()
    uids=[]
    for document in cursor:
        if document['User'][0]['uid'] in uids:
            continue
        newcoll.insert_one(document)
        uids.append(document['User'][0]['uid'])
def printkeynum():
    pcoll=db['NongGuanJiaByProblem']
    cursor=pcoll.find()
    for document in cursor:
        document['keywordsnum']=0
        if len(document['reply'])>0:
            for reply in document['reply']:
                if len(reply['keyword'])>0:
                    for keyword in reply['keyword']:
                        document['keywordsnum']+=1
        print(document['keywordsnum'])
def countdisaster():
    pcoll=db['NongGuanJiaByProblem']
    ynzz,zbbh=[],[]
    cursor=pcoll.find()

    for document in cursor:
        try:
            if document['keywordNum']!=-1:
                pass
        except KeyError:
            print("not set")
            document['keywordNum'] = 0
            if len(document['reply']) > 0:
                for reply in document['reply']:
                    if len(reply['keyword']) > 0:
                        for keyword in reply['keyword']:
                             if keyword["type"]=="zbbh":
                                 zbbh.append(keyword["keyword"])
                             elif keyword["type"]=="ynzz":
                                 ynzz.append(keyword["keyword"])
                             document['keywordNum'] +=1
                pcoll.update_one(
                    {"_id":document["_id"]},
                    {
                        "$set": {
                            "keywordNum": document['keywordNum']
                        }
                    }

                )
            else:
                pcoll.update_one(
                    {"_id":document["_id"]},
                    {
                        "$set": {
                            "keywordNum": 0
                        }
                    }

                )
    print(len(zbbh))
    print(len(ynzz))
    newzbbh = list(set(zbbh))
    newynzz= list(set(ynzz))
    print(len(newzbbh))
    print(len(newynzz))
def _100problemUser():
    ucoll=db['NongGuanJiaByUser']
    cursor = ucoll.find()
    userdicts=[]
    for document in cursor:
        if document['User'][0]['province']=="山东省":
            if document['User'][0]['city']=="潍坊市":
                if len(document['Question'])>100:
                    print(document['User'][0]['uid']+" "+str(len(document['Question'])))
                    userdict={"id":document['User'][0]['uid'],"problemsnum":len(document['Question']),"problemids":[]}
                    for question in document['Question']:
                        if question['keywordNum']>0:
                            userdict["problemids"].append(question['qid'])
                    userdicts.append(userdict)
                    import json
                    todrawproblems = open("./todrawproblems.json", 'w')
                    json.dump(
                        userdicts,
                        todrawproblems,
                        indent=4,
                        sort_keys=False,
                        ensure_ascii=False)
                    todrawproblems.close()
#_100problemUser()
def drawKeywordNum():
    import matplotlib.pyplot as plt
    from pylab import mpl
    from pandas import Series
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False

    client = MongoClient()
    db = client['NongGuanJia']
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    keywordNumList = []
    for document in cursor:
        keywordNumList.append(document['keywordNum'])

    pdkeywordNumList = Series(keywordNumList)
    mean_keywordNum = pdkeywordNumList.mean()

    plt.xlim(0, 71)
    plt.ylim(0, 400000)
    plt.title("keyword数量分步")
    plt.xlabel("keyword数量")
    plt.ylabel("keyword数量分步数")
    plt.hist(pdkeywordNumList, bins=60)
    plt.vlines(mean_keywordNum, 0, 500, color='red', label='平均keyword数量', linewidth=1.5, linestyle='--')
    plt.legend()
    plt.show()
def printKeyNum():
    client = MongoClient()
    db = client['NongGuanJia']
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    keynumdict={}
    for i in range(71):
        keynumdict[i]=0
    for document in cursor:
        keynumdict[document['keywordNum']]+=1
    print(keynumdict)
def addkeylink():
    client = MongoClient()
    db = client['NongGuanJia']
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    for document in cursor:
        if document['keywordNum']==0:
            continue
        else:
            for answer in document['reply']:
                if len(answer['keyword'])==0:
                    continue
                else:
                    for keyword in answer['keyword']:
                        if keyword['type']=='zbbh':
                            keyword['link']='http://ngjv4.laodao.so/api/pub/cropdisease.ashx?action=info&disid='+str(keyword['keyvalue'])
                        else:
                            keyword['link']='http://ngjv4.laodao.so/ashx/dd/dd_DifficultDis.ashx?action=info&ID='+str(keyword['keyvalue'])
            pcoll.update_one(
                        {"_id":document["_id"]},
                        {
                            "$set": {
                                "reply": document['reply']
                            }
                        }

                    )
def updateuser():
    ucoll=db['NongGuanJiaByUser']
    cursor = ucoll.find()
    for document in cursor:
        if len(document['Question'])==0:
            continue
        else:
            questions = document['Question']
            for question in document['Question']:
                index=document['Question'].index(question)
                question['keywordNum']=0
                if len(question['reply']) > 0:
                    for reply in question['reply']:
                        if len(reply['keyword']) > 0:
                            for keyword in reply['keyword']:
                                 question['keywordNum'] +=1
                    ucoll.update_one(
                        {"_id":document["_id"]},
                        {
                            "$set": {
                                'Question.'+str(index)+'.keywordNum': question['keywordNum']
                            }
                        }

                    )
                else:
                    pass

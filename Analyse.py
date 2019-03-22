from pymongo import MongoClient
from collections import Counter
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
                        #print(keyword['keyword'])
        print(document['keywordsnum'])
def countdisaster():
    pcoll=db['NongGuanJiaByProblem']
    ynzz,zbbh=[],[]
    cursor=pcoll.find()
    maxnum=0
    for document in cursor:
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
        if document['keywordNum']>maxnum:
            maxnum=document['keywordNum']
    print(maxnum)
    print(len(zbbh))
    print(len(ynzz))
    newzbbh = list(set(zbbh))
    newynzz= list(set(ynzz))
    print(len(newzbbh))
    print(len(newynzz))
#countdisaster()
ucoll=db['NongGuanJiaByUser']
cursor = ucoll.find()
for document in cursor:
    if document['User'][0]['province']=="山东省":
        if document['User'][0]['city']=="潍坊市":
            if len(document['Question'])>100:
                print(document['User'][0]['uid']+" "+str(len(document['Question'])))
# if keyword['keyword'] in dname:
#     print("yes")
# else:
#     if keyword['type']=='ynzz':
#         print("no"+str(keyword))
#         print(document['qid'])

# result=Counter(dname)
#print(result)
# print(len(dname))
# newqids = list(set(dname))
# for document in cursor:
#     print(dname.count(document["Name"]))
# print(len(newqids))














# newcoll=db['NongGuanJiaByProblem']
# nncoll=db['NongGuanJiaByProblemNew']
# nnn=db['NongGuanJiaByPNew']
# cursor=newcoll.find()
# qids=[]
#
# for document in cursor:
#     qids.append(document['qid'])
# print(len(qids))
# newqids = list(set(qids))
# print(len(newqids))
    # if len(document['Question'])>0:
    #     for question in document['Question']:
    #         nnn.insert_one(question)

# for document in cursor:
#     if len(document['Question'])>0:
#         #value=0
#         for question in document['Question']:
#             if question['qid']==0:
#                 #print(len(document['Question']))
#                 document['Question'].remove(question)
#                 #value=1
#                 coll.update_one(
#                     {"_id": document['_id']},
#                     {"$set": {"Question": document['Question']}}
#                 )
#
#                 print(document['_id'])
        # if value==1:
        #     nnn.insert_one(document)
        # value=0
       # print(len(document['Question']))
    #print(document['qid'])
    # if document['qid'] in qids:
    #     if document['recount']==14:
    #         print(document['question'])
    #     continue
    #nncoll.insert_one(document)
    #qids.append(document['qid'])
#
# print(len(qids))
# newqids = list(set(qids))
# print(len(newqids))
#     if len(document['Question'])>100:
#         print(document['User'][0]['uid'])
#         print(document['Question'])
    #break
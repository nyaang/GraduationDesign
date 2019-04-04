from pymongo import MongoClient
client = MongoClient()
db = client['NongGuanJia']


def countdisaster():
    pcoll = db['NongGuanJiaByProblem']
    ynzz, zbbh = [], []
    cursor = pcoll.find()

    for document in cursor:
        # try:
        #     if document['keywordNum']!=-1:
        #         pass
        # except KeyError:
        #    print("not set")
        document['keywordNum'] = 0
        if len(document['reply']) > 0:
            for reply in document['reply']:
                if len(reply['keyword']) > 0:
                    for keyword in reply['keyword']:
                        if keyword["type"] == "zbbh":
                            zbbh.append(keyword["keyword"])
                        elif keyword["type"] == "ynzz":
                            ynzz.append(keyword["keyword"])
                        document['keywordNum'] += 1
            # pcoll.update_one(
            #     {"_id":document["_id"]},
            #     {
            #         "$set": {
            #             "keywordNum": document['keywordNum']
            #         }
            #     }
            #
            # )
        else:
            # pcoll.update_one(
            #     {"_id":document["_id"]},
            #     {
            #         "$set": {
            #             "keywordNum": 0
            #         }
            #     }
            #
            # )
            pass
    print(len(zbbh))
    print(len(ynzz))
    newzbbh = list(set(zbbh))
    newynzz = list(set(ynzz))
    print(len(newzbbh))
    print(len(newynzz))
# countdisaster()


def _100problemUser():
    ucoll = db['NongGuanJiaByUser']
    cursor = ucoll.find()
    userdicts = []
    for document in cursor:
        if document['User'][0]['province'] == "山东省":
            if document['User'][0]['city'] == "潍坊市":
                if len(document['Question']) > 100:
                    print(document['User'][0]['uid'] + " " +
                          str(len(document['Question'])))
                    userdict = {
                        "id": document['User'][0]['uid'],
                        "problemsnum": len(
                            document['Question']),
                        "problemids": []}
                    for question in document['Question']:
                        if question['keywordNum'] > 0:
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
# _100problemUser()


def addkeylink():
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    for document in cursor:
        if document['keywordNum'] == 0:
            continue
        else:
            for answer in document['reply']:
                if len(answer['keyword']) == 0:
                    continue
                else:
                    for keyword in answer['keyword']:
                        if keyword['type'] == 'zbbh':
                            keyword['link'] = 'http://ngjv4.laodao.so/api/pub/cropdisease.ashx?action=info&disid=' + str(
                                keyword['keyvalue'])
                        else:
                            keyword['link'] = 'http://ngjv4.laodao.so/ashx/dd/dd_DifficultDis.ashx?action=info&ID=' + str(
                                keyword['keyvalue'])
            pcoll.update_one(
                {"_id": document["_id"]},
                {
                    "$set": {
                        "reply": document['reply']
                    }
                }

            )


def updateuser():
    ucoll = db['NongGuanJiaByUser']
    cursor = ucoll.find()
    for document in cursor:
        if len(document['Question']) == 0:
            continue
        else:
            for question in document['Question']:
                index = document['Question'].index(question)
                question['keywordNum'] = 0
                if len(question['reply']) > 0:
                    for reply in question['reply']:
                        if len(reply['keyword']) > 0:
                            for keyword in reply['keyword']:
                                question['keywordNum'] += 1
                    ucoll.update_one(
                        {"_id": document["_id"]},
                        {
                            "$set": {
                                'Question.' + str(index) + '.keywordNum': question['keywordNum']
                            }
                        }

                    )
                else:
                    pass


def exportdisater():
    pcoll = db['NongGuanJiaByProblem']
    ynzz, zbbh = [], []
    cursor = pcoll.find()

    for document in cursor:
        if document['keywordNum'] > 0:
            for reply in document['reply']:
                if len(reply['keyword']) > 0:
                    for keyword in reply['keyword']:
                        if keyword["type"] == "zbbh":
                            zbbh.append({
                                "link": keyword["link"],
                                "keyword": keyword["keyword"]
                            })
                        elif keyword["type"] == "ynzz":
                            ynzz.append({
                                "link": keyword["link"],
                                "keyword": keyword["keyword"]
                            })
    print(len(zbbh))
    print(len(ynzz))
    seen = set()
    newzbbh = []
    for d in zbbh:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            newzbbh.append(d)
    yseen = set()
    newynzz = []
    for d in ynzz:
        t = tuple(d.items())
        if t not in yseen:
            yseen.add(t)
            newynzz.append(d)
    print(len(newzbbh))
    print(len(newynzz))
    import json
    zbbhfile = open("./zbbhfile.json", 'w')
    json.dump(
        newzbbh,
        zbbhfile,
        indent=4,
        sort_keys=False,
        ensure_ascii=False)
    zbbhfile.close()
    ynzzfile = open("./ynzzfile.json", 'w')
    json.dump(
        newynzz,
        ynzzfile,
        indent=4,
        sort_keys=False,
        ensure_ascii=False)
    ynzzfile.close()
# exportdisater()

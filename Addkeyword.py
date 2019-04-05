from pymongo import MongoClient
import copy
client = MongoClient()
db = client['NongGuanJia']
zbbhcoll = db['NongGuanJiazbbh']
ynzzcoll = db['NongGuanJiaynzz']
zbbhs, ynzzs = [], []
cursor = zbbhcoll.find()
for zbbh in cursor:
    zbbhs.append(zbbh['Name'])
cursor = ynzzcoll.find()
for ynzz in cursor:
    ynzzs.append(ynzz['keyword'])
zbbhsets = list(set(zbbhs))
ynzzssets = list(set(ynzzs))

fatherkeywordsdict, fatherkeywordslist = {}, []
for keyword in zbbhsets:
    zbbhsetscopy = copy.deepcopy(zbbhsets)
    zbbhsetscopy.remove(keyword)
    for leftkeyword in zbbhsetscopy:
        if leftkeyword.find(keyword) != -1:
            fatherkeywordslist.append(leftkeyword)
            fatherkeywordsdict[leftkeyword] = []
fatherkeywordslist = list(set(fatherkeywordslist))
for keyword in zbbhsets:
    zbbhsetscopy = copy.deepcopy(zbbhsets)
    zbbhsetscopy.remove(keyword)
    for leftkeyword in zbbhsetscopy:
        if leftkeyword.find(keyword) != -1:
            fatherkeywordsdict[leftkeyword].append(keyword)

ynzzfatherkeywordsdict, ynzzfatherkeywordslist = {}, []
for keyword in ynzzssets:
    ynzzsetscopy = copy.deepcopy(ynzzssets)
    ynzzsetscopy.remove(keyword)
    for leftkeyword in ynzzsetscopy:
        if leftkeyword.find(keyword) != -1:
            ynzzfatherkeywordslist.append(leftkeyword)
            ynzzfatherkeywordsdict[leftkeyword] = []
ynzzfatherkeywordslist = list(set(ynzzfatherkeywordslist))
for keyword in ynzzssets:
    ynzzsetscopy = copy.deepcopy(ynzzssets)
    ynzzsetscopy.remove(keyword)
    for leftkeyword in ynzzsetscopy:
        if leftkeyword.find(keyword) != -1:
            ynzzfatherkeywordsdict[leftkeyword].append(keyword)


def disasterjudge(content=''):
    localzbbh = copy.deepcopy(zbbhsets)
    foundkeyword = []
    for fatherkeyword in fatherkeywordslist:
        if content.find(fatherkeyword) != -1:
            foundkeyword.append({'keyword': fatherkeyword,
                                 'type': 'zbbh',
                                 'taged': True,
                                 'keyvalue': None,
                                 'link': None})
            try:
                localzbbh.remove(fatherkeyword)
            except ValueError:
                pass
            for childkeyword in fatherkeywordsdict[fatherkeyword]:
                try:
                    localzbbh.remove(childkeyword)
                except ValueError:
                    pass
        else:
            pass
    for keyword in localzbbh:
        if content.find(keyword) != -1:
            foundkeyword.append({'keyword': keyword,
                                 'type': 'zbbh',
                                 'taged': True,
                                 'keyvalue': None,
                                 'link': None})

    localynzz = copy.deepcopy(ynzzssets)
    for fatherkeyword in ynzzfatherkeywordslist:
        if content.find(fatherkeyword) != -1:
            foundkeyword.append({'keyword': fatherkeyword,
                                 'type': 'ynzz',
                                 'taged': True,
                                 'keyvalue': None,
                                 'link': None})
            try:
                localynzz.remove(fatherkeyword)
            except ValueError:
                pass
            for childkeyword in ynzzfatherkeywordsdict[fatherkeyword]:
                try:
                    localynzz.remove(childkeyword)
                except ValueError:
                    pass
        else:
            pass
    for keyword in localynzz:
        if content.find(keyword) != -1:
            foundkeyword.append({'keyword': keyword,
                                 'type': 'ynzz',
                                 'taged': True,
                                 'keyvalue': None,
                                 'link': None})

    return foundkeyword
# disasterjudge()


def addkeyword():
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    keywordNumMax = 0
    for document in cursor:
        if document['keywordNum'] > 0:
            continue
        else:
            keywordNum = 0
            if len(document['reply']) > 0:
                for reply in document['reply']:
                    foundkeyword = disasterjudge(reply['content'])
                    if len(foundkeyword) > 0:
                        keywordNum += len(foundkeyword)
                        reply['keyword'] = foundkeyword
                if keywordNum > 0:
                    if keywordNum > keywordNumMax:
                        keywordNumMax = keywordNum
                        print(keywordNumMax)
                    document['keywordNum'] = keywordNum
                    # print(document)
                    pcoll.update_one(
                        {"_id": document["_id"]},
                        {
                            "$set": {
                                "keywordNum": document['keywordNum'],
                                "reply": document['reply'],
                                "taged": True
                            }
                        }

                    )
            else:
                pass
# addkeyword()

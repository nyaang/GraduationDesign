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
fatherkeywordsdict,fatherkeywordslist={},[]
for keyword in zbbhsets:
    zbbhsetscopy=copy.deepcopy(zbbhsets)
    zbbhsetscopy.remove(keyword)
    for leftkeyword in zbbhsetscopy:
        if leftkeyword.find(keyword) != -1:
            fatherkeywordslist.append(leftkeyword)
            fatherkeywordsdict[leftkeyword]=[]
fatherkeywordslist=list(set(fatherkeywordslist))
for keyword in zbbhsets:
    zbbhsetscopy=copy.deepcopy(zbbhsets)
    zbbhsetscopy.remove(keyword)
    for leftkeyword in zbbhsetscopy:
        if leftkeyword.find(keyword) != -1:
            fatherkeywordsdict[leftkeyword].append(keyword)
print(fatherkeywordsdict)
def disasterjudge(content=''):
    localzbbh=copy.deepcopy(zbbhsets)
    foundkeyword=[]
    #print(len(foundkeyword))
    for fatherkeyword in fatherkeywordslist:
        if content.find(fatherkeyword)!=-1:
            foundkeyword.append(fatherkeyword)
            localzbbh.remove(fatherkeyword)
            for childkeyword in fatherkeywordsdict[fatherkeyword]:
                try:
                    localzbbh.remove(childkeyword)
                except ValueError:
                    pass
        else:pass
    for keyword in localzbbh:
        if content.find(keyword)!=-1:
            foundkeyword.append(keyword)

    return foundkeyword
#disasterjudge()


def addkeyword():
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    for document in cursor:
        if document['keywordNum'] > 0:
            continue
        else:
            if len(document['reply']) > 0:
                for reply in document['reply']:
                    # print(reply['content'])
                    foundkeyword=disasterjudge(reply['content'])
                    if len(foundkeyword)>0:
                        print(foundkeyword)
addkeyword()
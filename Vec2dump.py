from pymongo import MongoClient
client = MongoClient()
db = client['NongGuanJia']
ucoll=db['NongGuanJiaByUser']
cursor = ucoll.find()
def countnodesandvectors():
    uids,qids,nodes=[],[],[]
    for document in cursor:
        if len(document['Reply'])==0:
            continue
        else:
            uids.append(int(document['User'][0]['uid']))
            for reply in document['Reply']:
                qids.append(reply['qid'])
                nodes.append(int(document['User'][0]['uid']+str(reply['qid'])))
    uids,qids=list(set(uids)),list(set(qids))
    print(len(uids),len(qids),len(nodes))


    uids2,qids2,nodes2=[],[],[]
    pcoll=db['NongGuanJiaByProblem']
    cursor2 = pcoll.find()
    for document in cursor2:
        if len(document['reply'])==0:
            continue
        else:
            qids2.append(document['qid'])
            for reply in document['reply']:
                uids2.append(reply['ruid'])
                nodes2.append(int(str(reply['ruid'])+str(document['qid'])))
    uids2,qids2=list(set(uids2)),list(set(qids2))
    print(len(uids2),len(qids2),len(nodes2))

# countnodesandvectors()
def dumpdatafile():
    node2vecfile=open('node2vecdata.txt','w')
    hin2vecfile=open('hin2vecdata.txt','w')
    hin2vecfile.write('#source_node	source_class	dest_node	dest_class	edge_class\n')
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    for document in cursor:
        if len(document['reply'])==0:
            continue
        else:
            for reply in document['reply']:
                hin2vecfile.write(str(reply['ruid'])+'	U	'+str((document['qid']+140000))+'	Q	U-Q\n')
                node2vecfile.write(str(reply['ruid'])+' '+str((document['qid']+140000))+'\n')
    hin2vecfile.close()
    node2vecfile.close()
dumpdatafile()
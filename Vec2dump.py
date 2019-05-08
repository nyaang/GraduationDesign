from pymongo import MongoClient
client = MongoClient()
db = client['NongGuanJia']
ucoll=db['NongGuanJiaByUser']
def dumpdatafile():
    cursor = ucoll.find()
    node2vecfile=open('node2vecdata.txt','w')
    hin2vecfile=open('hin2vecdata.txt','w')
    hin2vecfile.write('#source_node	source_class	dest_node	dest_class	edge_class\n')
    for document in cursor:
        if len(document['Reply'])==0:
            continue
        else:
            for reply in document['Reply']:
                hin2vecfile.write(document['User'][0]['uid']+'	U	'+str((reply['qid']+140000))+'	Q	U-Q\n')
                node2vecfile.write(document['User'][0]['uid']+' '+str((reply['qid']+140000))+'\n')
    hin2vecfile.close()
    node2vecfile.close()
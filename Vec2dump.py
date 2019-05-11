from pymongo import MongoClient
client = MongoClient()
db = client['NongGuanJia']
def countnodesandvectors():
    ucoll = db['NongGuanJiaByUser']
    cursor = ucoll.find()
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
# dumpdatafile()

def dataclean():
    # hin2vecfile = open('Result/hin2vecdata_P.txt', 'r')
    # u_pvecs = hin2vecfile.readlines()
    # hin2vecfile.close()
    # problem_user, problemlist = {}, []
    # for i in range(1, len(u_pvecs)):
    #     u_pvec = u_pvecs[i].split()
    #     problemlist.append(u_pvec[2])
    #
    # problemlist = list(set(problemlist))
    # for pid in problemlist:
    #     problem_user[pid] = []
    # for i in range(1, len(u_pvecs)):
    #     u_pvec = u_pvecs[i].split()
    #     problem_user[u_pvec[2]].append(u_pvec[0])
    #
    # lendict,lenlist={},[]
    # for pid in problemlist:
    #     lenlist.append(len(problem_user[pid]))
    # lenlist=list(set(lenlist))
    # lenlist.sort()
    # for lenghth in lenlist:
    #     lendict[lenghth]=0
    # for pid in problemlist:
    #     lendict[len(problem_user[pid])]+=1
    # print(lendict)
    #
    # cleanproblemfile=open('hin2vecdata_P_cleaned.txt','w')
    # problemlist.sort()
    # left_problems=0
    # for problemid in problemlist:
    #     if len(problem_user[problemid])>12:
    #         left_problems+=1
    #         for userid in problem_user[problemid]:
    #             cleanproblemfile.write(str(problemid) + '	Q	' + str(userid) + '	U	Q-U\n')
    # print(left_problems)
    # cleanproblemfile.close()
    #
    #
    # cleanproblemfile=open('hin2vecdata_P_cleaned.txt','r')
    # u_pvecs = cleanproblemfile.readlines()
    # cleanproblemfile.close()
    # user_problem, uidlist = {}, []
    # for i in range(0, len(u_pvecs)):
    #     u_pvec = u_pvecs[i].split()
    #     uidlist.append(u_pvec[2])
    #
    # uidlist = list(set(uidlist))
    # for uid in uidlist:
    #     user_problem[uid] = []
    # for i in range(0, len(u_pvecs)):
    #     u_pvec = u_pvecs[i].split()
    #     user_problem[u_pvec[2]].append(u_pvec[0])
    #
    # lendict,lenlist={},[]
    # print(len(uidlist))
    # for uid in uidlist:
    #     lenlist.append(len(user_problem[uid]))
    # lenlist=list(set(lenlist))
    # lenlist.sort()
    # for lenghth in lenlist:
    #     lendict[lenghth]=0
    # for uid in uidlist:
    #     lendict[len(user_problem[uid])]+=1
    # print(lendict)
    #
    # cleanuserfile=open('hin2vecdata_U_cleaned.txt','w')
    # uidlist_copy=[]
    # for uid in uidlist:
    #     uidlist_copy.append(int(uid))
    # uidlist_copy.sort()
    # uidlist=[]
    # for uid in uidlist_copy:
    #     uidlist.append(str(uid))
    # left_user,left_problem=0,[]
    # for uid in uidlist:
    #     if len(user_problem[uid])>5:
    #         left_user+=1
    #         for problemid in user_problem[uid]:
    #             left_problem.append(problemid)
    #             cleanuserfile.write(str(uid) + '	U	' + str(problemid) + '	Q	U-Q\n')
    # left_problem=list(set(left_problem))
    # print(left_user,len(left_problem))
    # cleanuserfile.close()

    hin2vecfile = open('hin2vecdata_U_cleaned.txt', 'r')
    u_pvecs = hin2vecfile.readlines()
    hin2vecfile.close()
    user_problem,uidlist={},[]
    for i in range(1, len(u_pvecs)):
        u_pvec = u_pvecs[i].split()
        uidlist.append(u_pvec[0])
    uidlist = list(set(uidlist))
    for uid in uidlist:
        user_problem[uid] = []
    for i in range(0, len(u_pvecs)):
        u_pvec = u_pvecs[i].split()
        user_problem[u_pvec[0]].append(u_pvec[2])
    problems,vectornums=[],0
    # node2vecfile = open('node2vecdata_cleaned.txt', 'w')
    uidlist_copy=[]
    for uid in uidlist:
        uidlist_copy.append(int(uid))
    uidlist_copy.sort()
    uidlist=[]
    for uid in uidlist_copy:
        uidlist.append(str(uid))
    for uid in uidlist:
        vectornums+=len(user_problem[uid])
        for pid in user_problem[uid]:
            # node2vecfile.write(uid+' '+pid+'\n')
    # node2vecfile.close()
            problems.append(pid)
    problems=list(set(problems))
    print(len(uidlist),len(problems),len(uidlist)+len(problems),vectornums)

# dataclean()
def user_problem():
    f=open('Result/node_vectors.txt','r')
    lines=f.readlines()
    f.close()
    userfile=open('user_vectors.txt','w')
    problemfile=open('problem_vectors.txt','w')
    uservectors,problemvectors=[],[]
    for i in range(1,len(lines)):
        # print(lines[i])
        vector=lines[i].split()
        if int(vector[0])<140000:
            uservectors.append(lines[i])
        else:
            problemvectors.append(lines[i])
    userfile.writelines(uservectors)
    problemfile.writelines(problemvectors)
    userfile.close()
    problemfile.close()
    print(len(uservectors),len(problemvectors))
# user_problem()
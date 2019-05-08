import math,random
class recommendation():
    def __init__(self):
        userfile=open('user_vectors.txt','r')
        uservectors=userfile.readlines()
        self.uservectordict,self.uservectorlist={},[]
        for uservector in uservectors:
            vector=uservector.split()
            self.uservectordict[vector[0]]=vector[1:]
            self.uservectorlist.append(vector[0])
        userfile.close()

        problemfile = open('problem_vectors.txt', 'r')
        problemvectors=problemfile.readlines()
        self.problemvectordict,self.problemvectorlist={},[]
        for problemvector in problemvectors:
            vector=problemvector.split()
            self.problemvectordict[vector[0]]=vector[1:]
            self.problemvectorlist.append(vector[0])
        problemfile.close()

        hin2vecfile=open('Result/hin2vecdata_P.txt','r')
        u_pvecs=hin2vecfile.readlines()
        self.user_problem,uidlist={},[]

        for i in range(1,len(u_pvecs)):
            u_pvec=u_pvecs[i].split()
            uidlist.append(u_pvec[0])
        # print(len(u_pveclist))
        uidlist=list(set(uidlist))
        for uid in uidlist:
            self.user_problem[uid]=[]
        for i in range(1,len(u_pvecs)):
            u_pvec=u_pvecs[i].split()
            self.user_problem[u_pvec[0]].append(u_pvec[2])
    def recommend(self):
        uids_recommend=[]
        for i in range(30):
            uids_recommend.append(random.choice(self.uservectorlist))
        successes,precisions,recalls=[],[],[]
        for uid in uids_recommend:
            qids=self.similar(uid)
            success=0.0
            for qid in qids:
                if qid in self.user_problem[uid]:
                    success+=1
            precision=success/14.0
            recall=success/len(self.user_problem[uid])
            successes.append(success)
            precisions.append(precision)
            recalls.append(recall)
            # print(success,precision,recall)
        print(float(sum(successes))/len(successes),float(sum(precisions))/len(precisions),float(sum(recalls))/len(recalls))

    def similar(self,uservectorid):
        uservector=self.uservectordict[uservectorid]
        similarvaldict,similarvallist={},[]
        for problemvectorid in self.problemvectorlist:
            problemvector=self.problemvectordict[problemvectorid]
            similarval=0
            for i in range(100):
                similarval=similarval+math.pow(abs(float(uservector[i])-float(problemvector[i])),100)
            similarvallist.append(similarval)
            similarvaldict[problemvectorid]=similarval
        similarvallist.sort()
        recommend_problems=[]
        for problemvectorid in self.problemvectorlist:
            if similarvaldict[problemvectorid]<=similarvallist[13]:
                recommend_problems.append(problemvectorid)
        return recommend_problems


r=recommendation()
for i in range(500):
    r.recommend()
# print(uservectordict['36761'])
# 每次推荐20个视频，每次推荐三十个用户，记录每个用户的准确率，每次推荐的评价准确率
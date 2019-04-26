def printKeyNum():
    from pymongo import MongoClient
    client = MongoClient()
    db = client['NongGuanJia']
    pcoll = db['NongGuanJiaByProblem']
    cursor = pcoll.find()
    keynumdict = {}
    for i in range(71):
        keynumdict[i] = 0
    for document in cursor:
        keynumdict[document['keywordNum']] += 1
    print(keynumdict)
# printKeyNum()


def drawKeywordNumA():
    import matplotlib.pyplot as plt
    from pylab import mpl
    import numpy as np
    from pandas import Series
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False

    keynumfenbuA = {
        "1": 23185,
        "2": 14315,
        "3": 10743,
        "4": 9336,
        "5": 8551,
        "6": 8014,
        "7": 7243,
        "8": 6635,
        "9": 5621,
        "10": 4777,
        "11": 4098,
        "12": 3487,
        "13": 2861}
    keywordNumList = []
    for i in range(1, 14):
        itimes = keynumfenbuA[str(i)] + 1
        for j in range(itimes):
            keywordNumList.append(i)

    pdkeywordNumList = Series(keywordNumList)

    plt.xlim(1, 13)
    plt.ylim(2500, 25000)
    plt.title("keyword数量分布", fontsize=20)
    plt.xlabel("keyword数量", fontsize=20)
    x_ticks = np.arange(1, 14, 1)
    plt.xticks(x_ticks)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylabel("keyword数量分布数", fontsize=20)
    plt.hist(pdkeywordNumList, bins=60)
    plt.legend()
    plt.show()
# drawKeywordNumA()


def drawKeywordNumB():
    import matplotlib.pyplot as plt
    from pylab import mpl
    import numpy as np
    from pandas import Series
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False

    keynumfenbuA = {
        "14": 2304,
        "15": 1815,
        "16": 1377,
        "17": 1073,
        "18": 868,
        "19": 623,
        "20": 508,
        "21": 380,
        "22": 265,
        "23": 231}
    keywordNumList = []
    for i in range(14, 24):
        itimes = keynumfenbuA[str(i)] + 1
        for j in range(itimes):
            keywordNumList.append(i)

    pdkeywordNumList = Series(keywordNumList)

    plt.xlim(14, 23)
    plt.ylim(0, 2400)
    plt.title("keyword数量分布", fontsize=20)
    plt.xlabel("keyword数量", fontsize=20)
    x_ticks = np.arange(14, 24, 1)
    y_ticks = np.arange(0, 2400, 230)
    plt.xticks(x_ticks, fontsize=20)
    plt.yticks(y_ticks, fontsize=20)
    plt.ylabel("keyword数量分布数", fontsize=20)
    plt.hist(pdkeywordNumList, bins=60)
    plt.legend()
    plt.show()
# drawKeywordNumB()

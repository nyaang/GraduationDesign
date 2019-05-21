from flask import Flask, request, render_template
from Similar import recommendation

app = Flask(__name__)
@app.route('/', methods=['GET'])
def login_form():
    return render_template('form.html')


@app.route('/login', methods=['POST'])
def login():
    userid = request.form['usernamelogin']
    r = recommendation()
    qids = r.similar(userid)
    from pymongo import MongoClient
    client = MongoClient()
    db = client['NongGuanJia']
    pcoll = db['NongGuanJiaByProblem']
    print(qids)
    questions = []
    for qid in qids:
        cursor = pcoll.find({"qid": int(qid) - 140000})
        for document in cursor:
            print(document)
            questions.append(document)
    for question in questions:
        question['url'] = 'http://www.laodao.so/forum/info/' + \
            str(question['qid'])
    return render_template('home.html', questions=questions, uid=userid)


if __name__ == '__main__':
    app.run()

## @package views
#
#  Routes and views for the flask application.
#

import time
import urllib.request
import json
import os
import random
from datetime import datetime

from flask import render_template, session , request , redirect , send_from_directory
from BlackHole import app
from BlackHole.objects import User , Game , Question

game = Game(datetime.now().strftime("%Y-%m-%d at %H:%M"), os.path.join("UsersData/"),111)
game.loadQuestions(os.path.join("games/"),"game1")

def userActive():
    return 'user' in session


#############################################################################################


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'manifest.json')


##############################################################################################


@app.route('/')
@app.route('/home')
def home(): 
    return render_template('index.html',Message='Invalid User')

@app.route('/userid')
def getUserId():
    if 'user' not in session:
        while True:
            suggestion = ""
            try:
                suggestion = str(json.loads(urllib.request.urlopen("https://api.namefake.com/").read().decode('utf-8'))['name']).split(' ', 1)[0]
            except:
                suggestion = game.fnames[random.randint(0,len(game.fnames)-1)]

            if '.' not in suggestion and "Prof" not in suggestion:
                user = User(suggestion,len(game.getQuestions()))

                if game.addUser(user):
                    session["user"] = user.__dict__
                    session['time'] = ""

                    filename = "UsersData/" + user.getId()
                    filename = os.path.join(app.root_path,filename)

                    with open(filename,"w") as fo:
                        fo.write(user.getId())
                        fo.write("\n")
                        fo.write(str(user.points))

                    return render_template('userid.html', userid = user.getId())

    return render_template('userid.html', userid =  User.dsobject(session['user']).getId())


##############################################################################################


@app.route('/question')
def question():
    if userActive() is not True: 
        return redirect('/')

    user = User.dsobject(session['user'])
    c = user.getCurrQuestion() 
    nqt = len(game.questions)

    if c == nqt:
        return redirect("/scores")

    q = game.questions[user.qindexs[c]]
    b = q.shuffleBranches()          

    return render_template('question.html', nq = nqt , trunk = q.getTrunk() , branches = b , leaf = q.getLeaf() , image = q.getImage() , alt = c )


##############################################################################################


@app.route('/checktime',methods = ['GET'])
def checkTime():
    if userActive() is not True: 
        return redirect('/')

    if request.method == 'GET':
        if session['time'] == '':
            session['time'] = str(request.args.get('time'))

        return render_template('checktime.html', time = session['time'])
        

##############################################################################################


@app.route('/evaluate',methods = ['GET'])
def evaluate():
    if userActive() is not True: 
        return redirect('/')

    if request.method == 'GET':
        render_template('checktime.html', time = '')

        session['time'] = ''
        user = User.dsobject(session['user'])
        user.currQuestion += 1

        if user.currQuestion > user.q:
            return render_template('evaluate.html', result = 'Finish')

        correct = request.args.get('c')            
        tseconds = request.args.get('time')

        if 'rue' in correct:
            user.addPoints(1/float(tseconds)*game.complexityFactor)

        user.answers.append(request.args.get('answer'))

        session["user"] = user.__dict__
        game.users[user.id] = user

        filename = "UsersData/" + user.getId()
        filename = os.path.join(app.root_path, filename)
        
        with open(filename,"w") as fo:
            fo.write(user.getId())
            fo.write("\n")
            fo.write(str(user.points))

        if user.currQuestion == user.q:
            return render_template('evaluate.html', result = 'Finish')
            
        return render_template('evaluate.html', result = 'Continue')


##############################################################################################


def getStats():
    data = {}
    curr_user = User.dsobject(session['user'])

    if len(curr_user.answers) >= curr_user.q:
        correct_answers = {}

        for q in game.questions:
            correct_answers[q.trunk] = 0

        for user in game.users.values():
            revQuestions = [None for i in range(len(user.answers))] 
            c = 0

            for i in user.qindexs:
                if i < len(user.answers):
                    revQuestions[i] = revQt(game.questions[i],user.answers[c])
                    c +=1

            for rqt in revQuestions:
                if rqt.answer == rqt.qt.leaf:
                    correct_answers[rqt.qt.trunk] += 1

        labels = []
        dataset = []
        c = 0

        for k,v in correct_answers.items():
            c += 1
            labels.append("P" + str(c))
            dataset.append(v)

        data = {'labels':labels,'datasets':[{"label":"Nr of Correct Answers",'data':dataset,"fill":1,"backgroundColor":"#68623B"}]}
    
    return data


##############################################################################################


@app.route('/scores')
def scores():
    if userActive() is not True: 
        return redirect('/')

    k,v = game.getUsers().keys(), game.getUsers().values()
    users = sorted(v,key=lambda user: user.points,reverse=True)

    try:
        if users[0].points > 0:
            for i in range(len(users)):
                users[i].percentage = users[i].points / users[0].points * 100     

        return render_template('scores.html',size=len(users),users=users,bardata = getStats())

    except Exception as e:
        print("No scores",e)

        if "list index out of range" in str(e):
            return render_template('scores.html',size=len(users),users=users,bardata = {})

        return render_template('scores.html',size=0,users=None)


##############################################################################################


class revQt(object):
    def __init__(self,qt,answer):
        self.qt = qt
        self.answer = answer

@app.route('/review')
def review():
    if userActive() is not True: 
        return redirect('/')

    user = User.dsobject(session['user'])

    if len(user.answers) >= user.q:
        revQuestions = [None for i in range(len(user.answers))] 
        c = 0

        for i in user.qindexs:
            revQuestions[i] = revQt(game.questions[i],user.answers[c])
            c +=1

        return render_template('review.html', rev = revQuestions, ln = len(revQuestions))
        
    return redirect("/")
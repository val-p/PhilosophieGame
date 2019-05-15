#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, url_for
from flask_caching import Cache
from getpage import getPage
from getpage import cache

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"

cache.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bonjour, monde !")

@app.route('/new-game', methods=['POST'])
def new_game():
    session['score'] = 0
    session['article'] = request.form['start'] 
    title1, link1 = getPage(session['article'])
    if title1 == 'Philosophie':
        flash('Congrats you won ! :) But try another page different from Philosophie', 'win')
        return redirect(url_for('index'))
    elif link1 == []:
        flash('Sorry ! You lost ! :(', 'lose')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('game'))


@app.route('/game', methods=['GET'])
def game():
    if session['article'] != 'Philosophie':
        title, link = getPage(session['article'])
        session['link'] = link
        if link == []:
            flash('Sorry you lost ! :(', 'lose')
            return redirect(url_for('index'))
        else:
            return render_template('game.html', link=link)
    else:
        flash('Congrats you won ! Final Score : ' + str(session['score']) + ' :)', 'win')
        return redirect(url_for('index'))

@app.route('/move', methods=['POST'])
def move():
    session['score'] = int(request.form['scoree']) + 1
    session['article'] = request.form['destination']                     
    return redirect(url_for('game'))

# Si vous définissez de nouvelles routes, faites-le ici

if __name__ == '__main__':
    app.run(debug=True)


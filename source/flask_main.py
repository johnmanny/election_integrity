# Authors: Taylor Santos, John Nemeth
# Description:
# Sources: 

from werkzeug.security import generate_password_hash, \
        check_password_hash
import flask
from flask import render_template
from flask import request
from flask import session
from flask import jsonify
from flask import url_for
from flask import flash
from flask import g
from flask import Markup
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

import os
import json
import logging
import uuid
from Crypto.PublicKey import RSA
from Crypto.Util import number

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# sets debug level for app
app.debug=True
app.logger.setLevel(logging.DEBUG)
app.secret_key="P3a9n71Dlb8Pkb3Qv481nk5PjnD"
APPLICATION_NAME = 'blog page'

# PW hash generation for admin page
password = "test"
pw_hash = generate_password_hash(password)

##### globals for election
maxVoters = 100
numCounters = 8

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), unique=True, nullable=False)
    pubkey = db.Column(db.String(300), unique=True, nullable=True)
    def __repr__(self):
        return '<User %r %r>' % (self.uuid, self.pubkey)

class VoteOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    index = db.Column(db.Integer, unique=True, nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    maxVoters = db.Column(db.Integer, unique=True, nullable=False)
    numCounters = db.Column(db.Integer, unique=True, nullable=False)
    primeMod = db.Column(db.String(100), unique=True, nullable=False)

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    uuid = db.Column(db.String(80), unique=True, nullable=False)
    pubkey = db.Column(db.String(300), unique=True, nullable=False)
    votes = db.Column(postgresql.ARRAY(db.String(100)), unique=False, nullable=False)
"""
class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), unique=True, nullable=False)
    pubkey = db.Column(db.String(300), unique=True, nullable=False)
    coefficients = 
"""

db.create_all()
if len(db.session.query(Settings).all()) != 1:
    db.session.query(Settings).delete()
    db.session.add(Settings(title="Untitled Vote", maxVoters=maxVoters, numCounters=numCounters,
        primeMod = str(number.getPrime((100**len(db.session.query(VoteOptions).all())).bit_length()+1))))
db.session.commit()

def get_user_id():
    user_id = session.get('uid')
    if not user_id:
        user_id = uuid.uuid4()
        flask.session['uid'] = user_id
    app.logger.debug(flask.session['uid']);
    return user_id

def get_or_add_uuid(voterid):
    user = db.session.query(User).filter_by(uuid=str(voterid)).first()
    if not user:
        user = User(uuid=voterid)
        db.session.add(user);
    return user
"""
###############################  Pages (routed from URLs)
"""
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("ENTERING INDEX")
    g.voterid = get_user_id()
    user = get_or_add_uuid(g.voterid)
    db.session.commit();
    app.logger.debug(User.query.all())
    app.logger.debug(flask.request.user_agent.string)
    app.logger.debug("LEAVING INDEX")

    return render_template('index.html')

@app.route("/vote")
def vote():
    # set session items for displaying
    g.voterid = get_user_id()
    g.vote_title = db.session.query(Settings).one().title
    g.vote_options = VoteOptions.query.all()
    if 'publickey' not in session:
        return render_template('vote_noregister.html')
    g.publickey = Markup('<p class="text-center">'\
    + '<textarea cols="63" rows="6" readonly style="resize:none; font-family:monospace">' \
    + session['publickey'].decode("ascii") \
    + '</textarea>' \
    + '</p>')
    g.maxval = int(db.session.query(Settings).one().primeMod)-1
    g.num_counters = db.session.query(Settings).one().numCounters

    return render_template('vote.html')

@app.route("/register")
def register():
    g.voterid = get_user_id()
    return render_template('register.html')

@app.route("/generate_key", methods=['POST'])
def generate():
    keyObj = RSA.generate(1024)
    privateKey = keyObj.exportKey()
    publicKey = keyObj.publickey().exportKey()
    session['privatekey'] = privateKey
    session['publickey'] = publicKey
    g.voterid = get_user_id()
    user = get_or_add_uuid(g.voterid)
    user.pubkey = publicKey.decode("ascii")
    db.session.commit();
    # newKey = RSA.importKey(privateKey)
    return '<p class="text-center">'\
        + '<textarea cols="63" rows="21" readonly style="resize:none; font-family:monospace">' \
        + publicKey.decode("ascii") \
        + '\n' \
        + privateKey.decode("ascii") \
        + '</textarea>' \
        + '</p>'

@app.route("/verify")
def verify():
    app.logger.debug("ENTERING VERIFICATION")
    g.voterid = get_user_id()
    return render_template('verify.html')

@app.route("/admin")
def admin():
    app.logger.debug("ENTERING ADMINISTRATION")
    g.vote_title = db.session.query(Settings).one().title
    g.vote_options = db.session.query(VoteOptions).all()
    return render_template('admin.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("page not found")
    return flask.render_template('not_found.html',
             badurl=request.base_url,
             linkback=url_for("index")), 404

"""
###############################  Html Form handlers
"""
#password checker
@app.route("/pc", methods=['POST'])
def pc():
    app.logger.debug("inside password checker")

    pw_attempt = flask.request.form["password"]
   
    if check_password_hash(pw_hash, pw_attempt):
        app.logger.debug("correct password entered: " + pw_attempt)
        flask.session['wp'] = True
    else:
        flask.flash('wrong password entered!')
        
    return flask.redirect(flask.url_for("admin"))

## submits the election attributes entered from administration page
# currently there is minimal error checking
@app.route("/save_settings", methods=['POST'])
def save_settings():
    app.logger.debug("saving settings")
    
    #gather form attributes
    title = request.form["title"]
    app.logger.debug("election title: " + title)
   
    voting_options = request.form.getlist("option")
    app.logger.debug("vote options: " + str(voting_options))
    db.session.query(VoteOptions).delete()
    db.session.query(Settings).delete()
    index = 0
    for option in voting_options:
        if option != "":
            entry = db.session.query(VoteOptions).filter_by(name=option).first()
            if not entry:
                db.session.add(VoteOptions(name=option, index=index))
                index += 1
    if len(db.session.query(VoteOptions).all()) < 2:
        db.session.query(VoteOptions).delete()
        db.session.add(VoteOptions(name="1"))
        db.session.add(VoteOptions(name="2"))

    db.session.add(Settings(title=title, maxVoters=100, numCounters=8,
        primeMod=str(number.getPrime((100**len(db.session.query(VoteOptions).all())).bit_length()+1))))
    db.session.commit()
    g.voterid = get_user_id()
    return render_template("index.html")

@app.route("/vote_send", methods=['POST'])
def vote_send():
    app.logger.debug('in vote_send()')
    g.vote_index  = request.form["votes"]
    g.coefficients = list(map(int, request.form.getlist("coefficients")))
    app.logger.debug(g.vote_index)
    app.logger.debug(g.coefficients)
    g.vote_name = db.session.query(VoteOptions).filter_by(index=g.vote_index).first().name
    g.max_voters = int(db.session.query(Settings).one().maxVoters)
    g.vote_value = g.max_voters**int(g.vote_index)
    g.voterid = get_user_id()
    g.vote_title = db.session.query(Settings).one().title
    g.vote_options = VoteOptions.query.all()
    if 'publickey' not in session:
        return render_template('vote_noregister.html')
    g.publickey = Markup('<p class="text-center">'\
    + '<textarea cols="63" rows="6" readonly style="resize:none; font-family:monospace">' \
    + session['publickey'].decode("ascii") \
    + '</textarea>' \
    + '</p>')
    g.num_counters = db.session.query(Settings).one().numCounters
    g.prime_modulo = int(db.session.query(Settings).one().primeMod)
    g.values_nomod = [g.vote_value + sum([g.coefficients[j] * i**(j+1) for j in range(len(g.coefficients))]) for i in range(1, g.num_counters+2)]
    g.values = [value % g.prime_modulo for value in g.values_nomod]
    vote = db.session.query(Votes).filter_by(uuid=str(g.voterid)).first()
    if not vote:
        vote = Votes(uuid=g.voterid, pubkey=session['publickey'].decode("ascii"), votes=list(map(str,g.values)))
        db.session.add(vote)
    else:
        vote.votes = g.values
    db.session.commit()
    return render_template("confirm_vote.html")

@app.route("/vote_confirm", methods=['POST'])
def vote_confirm():
    g.voterid = get_user_id()
    vote = db.session.query(Votes).filter_by(uuid=str(g.voterid)).first()
    vote.confirmed = True
    db.session.commit()
    return render_template("index.html")
"""
################################# main program area
"""
# app gets created so it'll exist if it's main or not
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

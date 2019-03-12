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
import os
import json
import logging
import uuid
from Crypto.PublicKey import RSA

app = flask.Flask(__name__)
# sets debug level for app
app.debug=True
app.logger.setLevel(logging.DEBUG)
app.secret_key="P3a9n71Dlb8Pkb3Qv481nk5PjnD"
APPLICATION_NAME = 'blog page'

# PW hash generation for admin page
password = "test"
pw_hash = generate_password_hash(password)

##### globals for election
title = "no vote"
voting_options = []
vote_count = 0

def get_user_id():
	user_id = session.get('uid')
	if not user_id:
		user_id = uuid.uuid4()
		flask.session['uid'] = user_id
	app.logger.debug(flask.session['uid']);
	return user_id

"""
###############################  Pages (routed from URLs)
"""
@app.route("/")
@app.route("/index")
def index():
	app.logger.debug("ENTERING INDEX")
	voterid = get_user_id()
	app.logger.debug(flask.request.user_agent.string)
	app.logger.debug("LEAVING INDEX")

	return render_template('index.html', voterid=voterid)

@app.route("/vote")
def vote():
	# set session items for displaying
	g.vote_title = title
	g.vote_options = voting_options
	g.vote_count = vote_count
	voterid = get_user_id()
	if 'publickey' not in session:
		return render_template('vote_noregister.html', voterid=voterid)
	pub = Markup('<p class="text-center">'\
	+ '<textarea cols="63" rows="6" readonly style="resize:none; font-family:monospace">' \
	+ session['publickey'].decode("ascii") \
	+ '</textarea>' \
	+ '</p>')
	return render_template('vote.html', voterid=voterid, publickey=pub, maxval=10000)

@app.route("/register")
def register():
	voterid = get_user_id()
			
	return render_template('register.html', voterid=voterid)

@app.route("/generate_key", methods=['POST'])
def generate():
	keyObj = RSA.generate(1024)
	privateKey = keyObj.exportKey()
	publicKey = keyObj.publickey().exportKey()
	session['privatekey'] = privateKey
	session['publickey'] = publicKey
	
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

	return render_template('verify.html')

@app.route("/admin")
def admin():
	app.logger.debug("ENTERING ADMINISTRATION")

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
@app.route("/vote_sub", methods=['POST'])
def vote_sub():
    app.logger.debug("inside vote attributes submission")
    
    #gather form attributes
    title = flask.request.form["title"]
    vote_count = flask.request.form["option_count"]
    app.logger.debug("number of voting options: " + vote_count)
    app.logger.debug("election title: " + title)
   
    voting_options.clear()
    for i in range(int(vote_count)):
        option_num = "option" + str(i)
        voting_options.append(flask.request.form[option_num])
        app.logger.debug(voting_options[i])
   
    return render_template("index.html")


"""
################################# main program area
"""
# app gets created so it'll exist if it's main or not
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

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

# if this were real solution, would obviously not set password here
password = "test"
pw_hash = generate_password_hash(password)


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
	voterid = get_user_id()
	return render_template('vote.html', voterid=voterid)

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
	
	newKey = RSA.importKey(privateKey)
	return jsonify([publicKey.decode("utf-8"), privateKey.decode("utf-8")]);

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
###############################  AJAX Request Handler 
"""
#--------------------NOT WORKING - NEED TO FIX
#password checker
@app.route("/pc", methods=['POST'])
def pc():
    app.logger.debug("GOT PASSWORD CHECK")

    pw_attempt = flask.request.form["password"]
   
    #gen_hash = generate_password_hash(pw_attempt + salt)
    #if gen_hash == pw_hash:
    if check_password_hash(pw_hash, pw_attempt):
        app.logger.debug("correct password entered: " + pw_attempt)
        #flask.g.wp = True
        flask.session['wp'] = True
    else:
        flask.flash('wrong password entered!')
        
    return flask.redirect(flask.url_for("admin"))
    #render_template("admin.html")



"""
################################# main program area
"""
# app gets created so it'll exist if it's main or not
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

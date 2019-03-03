# Authors: John Nemeth
# Description:
# Sources: 

import flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
#from flask import url_for
import json
import logging
import uuid

app = flask.Flask(__name__)
# sets debug level for app
app.debug=True
app.logger.setLevel(logging.DEBUG)
app.secret_key="P3a9n71Dlb8Pkb3Qv481nk5PjnD"
APPLICATION_NAME = 'blog page'

"""
###############################  Pages (routed from URLs)
"""
@app.route("/")
@app.route("/index")
def index():
	app.logger.debug("ENTERING INDEX")

	app.logger.debug("LEAVING INDEX")
	return render_template('index.html')

@app.route("/vote")
def vote():
	user_id = session.get('uid')
	if not user_id:
		flask.session['uid'] = uuid.uuid4()
	app.logger.debug(flask.session['uid']);
	return render_template('vote.html', voterid=flask.session['uid'])

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
	return flask.render_template('not_found.html', badurl=request.base_url, linkback=url_for("index")), 404


# app gets created so it'll exist if it's main or not
if __name__ == "__main__":
	app.run(port=8000,host="0.0.0.0")

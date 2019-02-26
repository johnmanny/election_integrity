# Authors: John Nemeth
# Description:
# Sources: 

import flask
from flask import render_template
from flask import request
from flask import session
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

# app gets created so it'll exist if it's main or not
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

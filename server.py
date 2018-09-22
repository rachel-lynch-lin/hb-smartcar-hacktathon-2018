from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask import jsonify
from flask_debugtoolbar import DebugToolbarExtension

# import pdb; pdb.set_trace()

app = Flask(__name__)

app.secret_key = ["SERVER_APP_SECRET_KEY"]
app.jinja_env.undefined = StrictUndefined

###############################################################################


@app.route('/job_list')
def job_list():
    """Job List Page"""

    return render_template('job_list.html')


@app.route('/job_details')
def job_details():
    """Job Details Page"""

    return render_template('job_details.html')



###############################################################################


if __name__ == "__main__":
    from server import app
    app.debug = True
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
from jinja2 import StrictUndefined
import requests

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

    job_1 = {
             "name": "Job 1",
             "car_address": "683 Sutter St, San Francisco, CA 94109",
             "dealership_address": "999 Van Ness Ave, San Francisco, CA 94109",
             "pick_up_time":"never"
            }
    job_2 = {
             "name": "Job 2",
             "car_address": "15215 N. Kierland Blvd, Scottsdale, AZ 85254",
             "dealership_address": "7014 E. Camelback Road, Suite #1210, Scottsdale, AZ 85251",
             "pick_up_time":"never"
            }
    job_3 = {
             "name": "Job 3",
             "car_address": "45500 Fremont Blvd Fremont, CA 94538",
             "dealership_address": "6701 Amador Plaza Road Dublin, CA 94568",
             "pick_up_time": "never"
            } 

    car_info = requests.get("https://192.168.2.45:8000/getinfo", verify=False)
    print(car_info)

    return render_template('job_list.html',
                           job_1=job_1,
                           job_2=job_2,
                           job_3=job_3)


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
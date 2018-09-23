import requests
import smartcar
import secrets
from twilio.rest import Client
from flask import Flask, request, jsonify, session, render_template, redirect, flash


account_sid = secrets.ACCOUNT_SID
auth_token = secrets.AUTH_TOKEN
smsClient = Client(account_sid, auth_token)
redirect_uri = secrets.REDIRECT_URI

app = Flask(__name__)
app.secret_key = 'blah!'
client = smartcar.AuthClient(
    client_id=secrets.CLIENT_ID,
    client_secret=secrets.CLIENT_SECRET,
    redirect_uri=redirect_uri,
    scope=['read_vehicle_info', 'read_location', 'read_odometer', 'control_security', 'read_vin']
)


@app.route('/', methods=['GET'])
def index():
    auth_url = client.get_auth_url(force=True)
    return '''
        <h1>Hello, Hackbright!</h1>
        <a href=%s>
          <button>Connect Car</button>
        </a>
    ''' % auth_url


@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    access = client.exchange_code(code)
    session['access_token'] = access['access_token']
    access_token = session['access_token']

    response = smartcar.get_vehicle_ids(access_token)
    print(response['vehicles'])
    session['vid'] = response['vehicles'][1]
    session['vin'] = smartcar.Vehicle(session['vid'], access_token).vin()
    return redirect('/security')


@app.route('/getlocation', methods=['GET'])
def getCarLocation():
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    print(access_token)
    location = vehicle.location()
    print(location)
    return jsonify(location)


@app.route('/getinfo', methods=['GET'])
def getInfo():
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    print(access_token)
    info = vehicle.info()
    print(info)
    return jsonify(info)


@app.route('/getodo', methods=['GET'])
def getOdo():
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    print(access_token)
    odometer = vehicle.odometer()
    return jsonify(odometer)


@app.route('/lock', methods=['GET'])
def lock():
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    response = vehicle.lock()
    print(response)
    return jsonify(response)


@app.route('/unlock', methods=['GET'])
def unlock():
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    response = vehicle.unlock()
    print(response)
    return jsonify(response)


@app.route('/security', methods=['GET'])
def security():
    return render_template('security.html')


@app.route('/pickup', methods=['GET'])
def pickup():
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    print(access_token)
    location = vehicle.location()
    print(location)
    lat = location.get("data").get("latitude")
    lng = location.get("data").get("longitude")
    loc = str(lat) + "," + str(lng)
    return render_template('pickup.html', location=loc, lat = lat, lng = lng)


@app.route('/sms', methods=['GET'])
def sms():
    message = smsClient.messages \
                .create(
                     body="Your car has arrived at the dealership!",
                     from_='+18316106841',
                     to='+14085325057'
                 )
    print(message.sid)
    return jsonify(message.sid)


@app.route('/job_list')
def job_list():
    """Job List Page"""

    job_1 = {
             "name": "Job 1",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - San Francisco",
             "car_address": "683 Sutter St, San Francisco, CA 94109",
             "dealership_address": "999 Van Ness Ave, San Francisco, CA 94109",
             "pick_up":"8:00AM"
            }
    job_2 = {
             "name": "Job 2",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - Scottsdale",
             "car_address": "15215 N. Kierland Blvd, Scottsdale, AZ 85254",
             "dealership_address": "7014 E. Camelback Road, Suite #1210, Scottsdale, AZ 85251",
             "pick_up":"10:30AM"
            }
    job_3 = {
             "name": "Job 3",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - Fremont",
             "car_address": "45500 Fremont Blvd Fremont, CA 94538",
             "dealership_address": "6701 Amador Plaza Road Dublin, CA 94568",
             "pick_up": "11:45AM"
            } 

    return render_template('job_list.html',
                           job_1=job_1,
                           job_2=job_2,
                           job_3=job_3)


@app.route('/job_list', methods=["POST"])
def show_job_details_page():
    """Job List Page"""

    return redirect('job_details.html')


@app.route('/job_details')
def job_details():
    """Job Details Page"""
    access_token = session.get('access_token')
    vid = session.get('vid')
    vehicle = smartcar.Vehicle(vid, access_token)
    print(access_token)
    location = vehicle.location()
    print(location)
    lat = location.get("data").get("latitude")
    lng = location.get("data").get("longitude")
    loc = str(lat) + "," + str(lng)

    job_1 = {
             "name": "Job 1",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - San Francisco",
             "car_address": "683 Sutter St, San Francisco, CA 94109",
             "dealership_address": "999 Van Ness Ave, San Francisco, CA 94109",
             "pick_up":"8:00AM"
            }


    return render_template('job_details.html', job_1=job_1, lat = lat, lng = lng)


@app.route('/job_details', methods=["POST"])
def show_dropoff_page():
    """Go to Job Dropoff Page"""
    

    job_1 = {
             "name": "Job 1",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - San Francisco",
             "car_address": "683 Sutter St, San Francisco, CA 94109",
             "dealership_address": "999 Van Ness Ave, San Francisco, CA 94109",
             "pick_up":"8:00AM"
            }
    message = smsClient.messages \
                .create(
                     body="Your car is on its way to the dealership!",
                     from_='+18316106841',
                     to='+14085325057'
                 )
    print(message.sid)

    return redirect('job_dropoff.html',
                    message=jsonify(message.sid))


@app.route('/dropoff')
def dropoff_details():
    """Dropoff Details Page"""
    lat = 37.784624 
    lng = -122.421524

    job_1 = {
             "name": "Job 1",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - San Francisco",
             "car_address": "683 Sutter St, San Francisco, CA 94109",
             "dealership_address": "999 Van Ness Ave, San Francisco, CA 94109",
             "pick_up":"8:00AM"
            }
     
    return render_template('job_dropoff.html',
                           job_1=job_1, lat = lat, lng = lng)


@app.route('/dropoff', methods=["POST"])
def show_job_completion_page():
    """Show job completion page"""
     
    return redirect('job_completion.html')


@app.route('/job_completion')
def job_completion():
    """Job Details Page"""
    

    job_1 = {
             "name": "Job 1",
             "customer_name": "Sahas",
             "dealership_name": "Tesla Dealership - San Francisco",
             "car_address": "683 Sutter St, San Francisco, CA 94109",
             "dealership_address": "999 Van Ness Ave, San Francisco, CA 94109",
             "pick_up":"8:00AM"
            }
     
    return render_template('job_completion.html',
                           job_1=job_1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context="adhoc")
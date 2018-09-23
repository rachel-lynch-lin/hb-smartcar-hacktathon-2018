
import smartcar
import secrets
from twilio.rest import Client
from flask import Flask, request, jsonify, session

account_sid = 'AC3af0ca72a75e372ab607702d7ca45c0f'
auth_token = 'e569a6f02d904b7f1840abcbcc92f849'
smsClient = Client(account_sid, auth_token)

app = Flask(__name__)
app.secret_key = 'blah!'
client = smartcar.AuthClient(
    client_id=secrets.CLIENT_ID,
    client_secret=secrets.CLIENT_SECRET,
    redirect_uri='https://192.168.2.45:8000/callback',
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
    session['vid'] = response['vehicles'][0]
    session['vin'] = smartcar.Vehicle(session['vid'], access_token).vin()
    print(session)
    print(access_token)
    return jsonify(access)

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

@app.route('/sms', methods=['GET'])
def sms():
    message = smsClient.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+18316106841',
                     to='+14085325057'
                 )
    print(message.sid)
    return jsonify(message.sid)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, ssl_context="adhoc")
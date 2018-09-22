
import smartcar
import secrets
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'blah!'
client = smartcar.AuthClient(
    client_id=secrets.CLIENT_ID,
    client_secret=secrets.CLIENT_SECRET,
    redirect_uri='http://localhost:8000/callback',
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

if __name__ == '__main__':
    app.run(port=8000)
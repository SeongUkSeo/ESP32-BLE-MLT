from flask import Flask, request, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from model.anomaly_detection import IamPlantAlgo, AnomalyText
from datetime import datetime, timedelta
import pandas as pd
import json, requests
from DataUtil import generate_sapflow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)
ESP32_IP = ''


class Users(db.Model):
    __tablename__ = 'users'
    sensorid = db.Column(db.String, primary_key=True)
    userid = db.Column(db.Integer)
    plantid = db.Column(db.Integer)
    plantname = db.Column(db.String)
    plantmeet = db.Column(db.String)
    # def __repr__(self):
    #     return '<SensorData %r>' % self.id
    
class Sensors(db.Model):
    __tablename__ = 'sensors'
    __table_args__ = (
        db.PrimaryKeyConstraint('timestamp', 'sensorid'),
    )
    timestamp = db.Column(db.DateTime, default=datetime.now())
    sensorid = db.Column(db.String)
    sapflow = db.Column(db.Integer)
    soilmoisture = db.Column(db.Integer)
    sunlight = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    errorcode = db.Column(db.Integer)

class Anomaly(db.Model):
    __tablename__ = 'anomaly'
    __table_args__ = (
        db.PrimaryKeyConstraint('timestamp', 'sensorid'),
    )
    timestamp = db.Column(db.DateTime, default=datetime.now())
    sensorid = db.Column(db.String)
    sapflow_activity = db.Column(db.Integer)
    sapflow = db.Column(db.Integer)
    soilmoisture = db.Column(db.Integer)
    sunlight = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)

SensorTypes = {
    'sapflow' : Sensors.sapflow,
    'soilmoisture' : Sensors.soilmoisture,
    'sunlight' : Sensors.sunlight,
    'temperature' : Sensors.temperature,
    'humidity' : Sensors.humidity,
}

@app.route('/')
def index():
    return render_template_string("""
        <html>
            <body>
                <h1>ESP32 LED Control</h1>
                <button id="onButton">Turn ON</button>
                <button id="offButton">Turn OFF</button>
                <script>
                    document.getElementById("onButton").addEventListener("click", function(event) {
                        fetch('/led', { 
                            method: 'POST', 
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: new URLSearchParams({state: 'ON'}) 
                        })
                        event.preventDefault();
                    });
                    document.getElementById("offButton").addEventListener("click", function(event) {
                        fetch('/led', { 
                            method: 'POST', 
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: new URLSearchParams({state: 'OFF'}) 
                        })
                        event.preventDefault();
                    });
                </script>
            </body>
        </html>
    """)

@app.route('/data-endpoint', methods=['POST'])
def add_sensor_data():
    id = request.form['ID']
    sapflow = generate_sapflow()
    temperature = request.form['TP']
    humidity = request.form['HM']
    sunlight = request.form['SN']
    soilmoisture = request.form['SM']
    errorcode = request.form['EC']
    data = Sensors(
        timestamp=datetime.now(),
        sensorid=id,
        sapflow=sapflow,
        soilmoisture=soilmoisture,
        sunlight=sunlight,
        temperature=temperature,
        humidity=humidity,
        errorcode=errorcode
    )
    db.session.add(data)
    db.session.commit()
    return 'OK', 200

@app.route('/led', methods=['POST'])
def led_control():
    state = request.form.get('state')
    if state in ['ON', 'OFF']:
        try:
            response = requests.get(f"http://{ESP32_IP}/led?state={state}")
            response.raise_for_status()
            return "LED state changed successfully", 200
        except requests.exceptions.HTTPError as errh:
            return f"Http Error: {errh}", 500
        except requests.exceptions.ConnectionError as errc:
            return f"Error Connecting: {errc}", 500
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error: {errt}", 500
        except requests.exceptions.RequestException as err:
            return f"Something went wrong: {err}", 500
    else:
        return "Invalid state. Please send 'ON' or 'OFF'.", 400

@app.route('/sensor-by-sensor', methods=['GET'])
def get_sensor_realtime():
    targetdate = datetime.now() - timedelta(weeks=1)
    userid = request.args.get('userid')
    plantid = request.args.get('plantid')
    sensortype = request.args.get('sensortype')
    target_sensor_ids = Users.query.filter_by( 
        userid=userid, plantid=plantid).with_entities(
        Users.sensorid
    ).all()
    target_sensor_id = target_sensor_ids[0][0]
    sensor_data = Sensors.query.filter(
        Sensors.sensorid==target_sensor_id,
        Sensors.errorcode==0,
        Sensors.timestamp>targetdate
        ).with_entities(
        Sensors.timestamp,
        SensorTypes[sensortype]
        ).order_by(Sensors.timestamp.desc()).all()
    print(len(sensor_data))
    sensor_divider = {
        'sapflow' : 1,
        'soilmoisture' : 40.95,
        'sunlight' : 40.95,
        'temperature' : 100,
        'humidity' : 100,
    }
    timestamp_list = []
    sensorvalue_list = []
    for ts,sv in sensor_data:
        timestamp_list.append(datetime.strftime(ts, '%Y-%m-%d %H:%M:%S'))
        sensorvalue_list.append(sv)
    df = pd.DataFrame({
        'timestamp' : timestamp_list,
        'sensorvalue' : sensorvalue_list
    })
    df['datehour'] = df['timestamp'].str.split(':', expand=True)[0]
    df['datehour'] += ':00:00'
    df = df[['datehour','sensorvalue']].groupby('datehour', as_index=False).mean()

    targetdate = datetime.strftime(targetdate, '%Y-%m-%d %H') + ':00:00'
    targetdate = datetime.strptime(targetdate, '%Y-%m-%d %H:%M:%S')
    retdf = pd.DataFrame(
        {
            "datehour" : pd.date_range(
                start=targetdate,
                end=targetdate+timedelta(weeks=1),
                freq='H' ).astype(str)
        }
    )
    retdf = pd.merge(retdf, df, how='left', on='datehour')
    return json.dumps(
        list(map(
        lambda x: {
            "timestamp":x[0],
            "sensorvalue":None if pd.isna(x[1]) else int(x[1] / sensor_divider[sensortype])
            }, retdf.values
        )))


@app.route('/sensor-by-user', methods=['GET'])
def get_sensor_byusers():
    userid = int(request.args.get('userid'))
    target_sensor_ids = Users.query.filter_by( 
        userid=userid).with_entities(
        Users.sensorid,
        Users.plantname,
        Users.plantmeet
        ).order_by(Users.plantid).all()
    user_sensor_data = []
    for sid in target_sensor_ids:
        sensor_data = Sensors.query.filter_by(
            sensorid=sid[0], errorcode=0).with_entities(
            Sensors.timestamp,
            Sensors.sapflow,
            Sensors.soilmoisture,
            Sensors.sunlight,
            Sensors.temperature,
            Sensors.humidity
            ).order_by(Sensors.timestamp.desc()).first()
        sensor_data = dict(zip(
            ['name', 'meetdate', 'timestamp','sapflow','soilmoisture','sunlight','temperature','humidity'],
            list(sid)[1:]+list(sensor_data)
            ))
        sensor_data['timestamp'] = datetime.strftime(
            sensor_data['timestamp'], '%Y-%m-%d %H:%M:%S'
            )
        sensor_data['meetdate'] = (
            datetime.now() - datetime.strptime(
            sensor_data['meetdate'], "%Y-%m-%d")
            ).days
        user_sensor_data.append(sensor_data)
    return json.dumps(user_sensor_data)
    
@app.route('/sensor-anomaly', methods=['GET'])
def get_sensor_anomaly():
    userid = int(request.args.get('userid'))
    target_sensor_ids = Users.query.filter_by( 
        userid=userid).with_entities(
        Users.sensorid
        ).order_by(Users.plantid).all()
    user_anomaly_data = []
    for sid in target_sensor_ids:
        anomaly_data = Anomaly.query.filter_by(
            sensorid=sid[0]).with_entities(
            Anomaly.timestamp,
            Anomaly.sapflow_activity,
            Anomaly.sapflow,
            Anomaly.soilmoisture,
            Anomaly.sunlight,
            Anomaly.temperature,
            Anomaly.humidity
            ).order_by(Anomaly.timestamp.desc()).first()
        if anomaly_data==None or (datetime.now() - anomaly_data[0]).total_seconds() > 3600:
        # if True:
            targetdate = datetime.now() - timedelta(weeks=1)
            sensor_data = Sensors.query.filter(
                Sensors.sensorid==sid[0],
                Sensors.errorcode==0,
                Sensors.timestamp>targetdate
                ).with_entities(
                Sensors.timestamp,
                Sensors.sapflow,
                Sensors.soilmoisture,
                Sensors.sunlight,
                Sensors.temperature,
                Sensors.humidity
                ).order_by(Sensors.timestamp.desc()).all()
            print(sid, len(sensor_data))
            anomaly_data = IamPlantAlgo(sensor_data)

            data = Anomaly(
                timestamp=datetime.now(),
                sensorid=sid[0],
                sapflow_activity=anomaly_data['sapflow_activity'],
                sapflow=anomaly_data['sapflow'],
                soilmoisture=anomaly_data['soilmoisture'],
                sunlight=anomaly_data['sunlight'],
                temperature=anomaly_data['temperature'],
                humidity=anomaly_data['humidity']
            )
            db.session.add(data)
            db.session.commit()
        else:
            anomaly_data = dict(zip(
            ['timestamp','sapflow_activity','sapflow','soilmoisture','sunlight','temperature','humidity'],
            list(anomaly_data)
            ))
            anomaly_data['timestamp'] = datetime.strftime(
                anomaly_data['timestamp'], '%Y-%m-%d %H:%M:%S'
            )
        guide_text = AnomalyText(anomaly_data)
        anomaly_data['guide_text'] = guide_text
        user_anomaly_data.append(anomaly_data)
    return json.dumps(user_anomaly_data)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

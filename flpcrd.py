from flask import Flask, jsonify
import json

app = Flask(__name__)

# 가상의 데이터베이스에 저장된 기기 정보
with open('./dataserver/device_data.json', 'r') as f:
        device_data = json.load(f)

latest_timestamp = []
for d in device_data:
    latest_timestamp.append(d['timestamp'])

@app.route('/get_updated_devices', methods=['GET'])
def get_updated_devices():
    with open('./dataserver/device_data.json', 'r') as f:
        loaded_data = json.load(f)
    updated_devices = []
    for index in range(8):
        if latest_timestamp[index]!=loaded_data[index]['timestamp']:
            updated_devices.append(loaded_data[index])
            latest_timestamp[index] = loaded_data[index]['timestamp']
            print(loaded_data[index]['expid'], end=', ')
    print()
    return jsonify(updated_devices)

@app.route('/get_initial_devices', methods=['GET'])
def get_initial_devices():
    with open('./dataserver/device_data.json', 'r') as f:
        loaded_data = json.load(f)
    return jsonify(loaded_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3333)


# from datetime import datetime
# import json
# import numpy as np
# import time

# key_list = ['sensorid',
#     'expid',
#     'timestamp',
#     'sapflow',
#     'soilmoisture',
#     'sunlight',
#     'temperature',
#     'humidity',
#     'errorcode']
# def gen_sensorid():
#     return ':'.join([hex(np.random.randint(16, 256))[2:].upper() for _ in range(6)])

# device_list = []

# for i in range(1, 9):
#     val_list = [gen_sensorid(),
#      i,
#      str(datetime.now())[:-7],
#      np.round(np.random.random() * 5,3),
#      np.round(np.random.random() * 50,2),
#      int(np.random.random() * 5000),
#      np.round(np.random.random() * 30,1),
#      np.round(np.random.random() * 100,1),
#      0]
#     device_list.append(dict(zip(key_list, val_list)))
# with open('./dataserver/device_data.json', 'w') as f:
#         json.dump(device_list, f)
        
# while True:
#     with open('./dataserver/device_data.json', 'r') as f:
#         loaded_data = json.load(f)
#     size = np.random.randint(1,4)
#     update_list = np.random.randint(0,8, size=size)
#     for i in update_list:
#         val_list = [loaded_data[i]['sensorid'],
#             loaded_data[i]['expid'],
#             str(datetime.now())[:-7],
#             np.round(np.random.random() * 5,3),
#             np.round(np.random.random() * 50,2),
#             int(np.random.random() * 5000),
#             np.round(np.random.random() * 30,1),
#             np.round(np.random.random() * 100,1),
#             0]
#         loaded_data[i] = dict(zip(key_list, val_list))
        
#     with open('./dataserver/device_data.json', 'w') as f:
#         json.dump(loaded_data, f)
#     time.sleep(10)

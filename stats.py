import api
import time
from datetime import datetime
from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from tqdm import tqdm

client = InfluxDBClient(url="http://127.0.0.1:8086", debug=False)


while True:
    laundry_logs_data = []
    machine_level_data = []
    for room_name, room_number in api.rooms.items():
        raw_data = api.get_room(room_number)
        if raw_data == -1:
            continue
        time_stamp = time.time() * 1000

        washer_point = Point("washers").tag('Room', room_name).field('value', int(raw_data['data']['wash_available'])/int(raw_data['data']['wash_total'])).time(time=datetime.utcnow())
        dryer_point = Point("dryers").tag('Room', room_name).field('value', int(raw_data['data']['dryer_available'])/int(raw_data['data']['dryer_total'])).time(time=datetime.utcnow())
        laundry_logs_data += [washer_point, dryer_point]

        
        for type in ['washers', 'dryers']:
            for machine in raw_data['data'][type]:
                left_time = '0' if machine['left_time'] == '' else str(machine['left_time'])
                data_point = Point(type).tag('Room', room_name).tag('Machine_Number', machine['label_id']).field('status', machine['satus']).field('left_time', left_time).field('status_text', machine['status_text'])
                machine_level_data += [data_point] 
    
    write_api = client.write_api(write_options=SYNCHRONOUS)
    if laundry_logs_data:
        write_api.write(bucket="laundry-logs", org="me", record=laundry_logs_data)
    if machine_level_data:
        write_api.write(bucket="laundry-machine-level", org="me", record=machine_level_data)
    time.sleep(60)




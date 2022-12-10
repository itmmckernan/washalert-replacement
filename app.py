from flask import Flask, request, render_template
from markupsafe import escape
import api
app = Flask(__name__)

@app.route('/')
def directory():
    return render_template('directory.html', room_groups=api.room_groups.keys())

@app.route('/all')
def overview_alls():
    rooms = api.get_rooms()
    return render_template('room.html', api_info=rooms, title="Room Overview")

@app.route('/byGroup/<string:room_group>')
def roomGroup(room_group):
    if room_group in api.room_groups.keys():
        room_dict = {}
        for room in api.room_groups[room_group]:
            room_dict[list(api.rooms.keys())[list(api.rooms.values()).index(room)]] = api.get_room(room)
        return render_template('room.html', api_info=room_dict, title=room_group)
    else:
        return "<h1>Error: Invalid room group</h1>"

@app.route('/byName/<string:room_name>')
def singleRoom(room_name):
    if room_name in api.rooms.keys():
        room_info = api.get_room(api.rooms[room_name])
        return render_template('room.html', api_info={room_name: room_info}, title=room_name)
    else:
        return "<h1>Error: Invalid room</h1>"

if __name__ == '__main__':
   app.run(debug=False, port=69420, host='0.0.0.0')
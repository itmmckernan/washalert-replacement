import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('secrets.ini')

headers={"X-API-KEY": config['Main']['api_key']}
base_url_room_status = "https://getwashconnect.com/api/rooms/room_status"
token = config['Main']['token']
location_id = "13046"
rooms = {'Yosemite - Tower 0': '1', 'Yosemite - Tower 2': '2', 'Yosemite - Tower 4': '3', 'Yosemite - Tower 5': '4', 'Yosemite - Tower 7': '5', 'Yosemite - Tower 9': '6', 'Sierra Madre - Tower 0': '7', 'Sierra Madre - Tower 1': '8', 'Sierra Madre - Tower 2': '9', 'Sierra Madre - Tower 3': '10', 'Sierra Madre - Tower 4': '11', 'Sierra Madre - Tower 5': '12', 'Tenaya - North Mtn': '13', 'Tenaya - South Mtn': '14', 'Sequoia - North Mtn': '15', 'Sequoia - South Mtn': '16', 'Muir - North Mtn': '17', 'Muir - South Mtn': '18', 'Santa Lucia - North Mtn': '19', 'Santa Lucia - South Mtn': '20', 'Trinity - North Mtn': '21', 'Trinity - South Mtn': '22', 'Whitney - North Mtn': '23', 'Palomar - North Mtn': '24', 'Diablo - North Mtn': '25', 'Cerro Vista - Morro': '26', 'Cerro Vista - Hollister': '27', 'Cerro Vista - Bishop': '28', 'Poly Canyon Village - Aliso': '29', 'Poly Canyon Village - Corralitos': '30', 'Poly Canyon Village - Dover': '31', 'Poly Canyon Village - Estrella': '32', 'Poly Canyon Village - Foxen': '33', 'Poly Canyon Village - Gypsum': '34', 'Poly Canyon Village - Huasna': '35', 'Poly Canyon Village - Inyo': '36', 'Yakitutu - Bldg A, A1-37': '37', 'Yakitutu - Bldg B, B1': '38', 'Yakitutu - Bldg C, C1-37': '39', 'Yakitutu - Bldg D, D1-39': '40', 'Yakitutu - Bldg E, E1-39': '41', 'Yakitutu - Bldg F, F1-37': '42', 'Yakitutu - Bldg G, G1-39': '43', 'Freemont Bldg 109': '44'}

room_groups = {
    "Cerro Vista": ["26", "27", "28"],
    "North Mountain": ["23", "24", "25"],
    "Poly Canyon Village": ["29", "30", "31", "32", "33", "34", "35", "36"],
    "Yosemite": ['1', '2', '3', '4', '5', '6'],
    "Sierra Madre": ["7", '8','9','10','11', '12']
}

def url_asm(baseurl, location_id, room_num, token):
    return f'{baseurl}?location_id={location_id}&room_number={room_num}&token={token}'

def authenticate():
    body = {
        'username': config['Main']['username'],
        'password': config['Main']['username'],
        'language': "1"
    }
    request = requests.post('https://getwashconnect.com/api/auth/login', headers=headers, body=body)
    global token
    if request.ok:
        try:
            token = json.loads(request.content)['token']
        except:
            pass

def get_room(room_num, level=0):
    try:
        return _get_room(room_num)
    except Exception("Unauthorized"):
        authenticate()
        get_room(room_num, level+1)
        if level > 5:
            raise Exception("Authentication Failure")



def _get_room(room_num):
    request = requests.get(url_asm(base_url_room_status, location_id, room_num, token), headers=headers, timeout=10)
    if request.ok:
        try:
            return json.loads(request.content)
        except ValueError:
            raise Exception(request.reason)
    else:
        raise Exception(request.reason)


def get_rooms(rooms=rooms):
    out_dict = {}
    for room_name, room_num in rooms.items():
        out_dict[room_name] = get_room(room_num)
    return out_dict

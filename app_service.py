from flask import Flask, request, render_template
import requests, os, psycopg2, bcrypt

DATABASE_URL = os.environ.get('DATABASE_URL','dbname=shopping_list')
api_key = open('maps.txt','r').read()
payload={}
headers = {}
place_id_dict = {}

def store_search_json(store):
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={store}&location=-33.814999%2C151.001114&radius=100000&strictbounds=true&key={api_key}"
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def get_place_id(response):
    return response['predictions'][0]['place_id']

def get_store_name(response):
    return response['predictions'][0]['structured_formatting']['main_text']

def store_place_details(place_id,store_name,user_id):
    url_for_details = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.request("GET",url_for_details,headers=headers,data=payload)
    latitude = response.json()['result']['geometry']['location']['lat']
    longitude = response.json()['result']['geometry']['location']['lng']
    destination = f"{latitude}%2C{longitude}"
    for component in response.json()['result']['address_components']:
        if 'locality' in component['types']:
            location = component['short_name']

    url_for_distance = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=-33.819450%2C151.004166&destinations={destination}&key={api_key}"
    response_for_distance = requests.request("GET", url_for_distance, headers=headers, data=payload)
    distance_from_origin = float(response_for_distance.json()['rows'][0]['elements'][0]['distance']['text'].split()[0])

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO stores_1(store_name,location,place_id,latitude,longitude,distance_from_origin,user_id) VALUES(%s,%s,%s,%s,%s,%s,%s)
    """,(store_name,location,place_id,latitude,longitude,distance_from_origin,user_id))
    conn.commit()
    cur.close()

# def all_store_distances(dict):
#     dest = ""
#     i = 0
#     for place,params in dict.items():
#         i += 1
#         if len(dict.items()) == i:
#             dest = dest + f"{params['latitude']}%2C{params['longitude']}"
#         else:
#             dest = dest + f"{params['latitude']}%2C{params['longitude']}%7C"
#     print(dest)
#     url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=-33.819450%2C151.004166&destinations={dest}&key={api_key}"
#     response = requests.request("GET", url, headers=headers, data=payload)

#     i = 0
#     for place,params in dict.items():
#         params['distance_from_origin'] = response.json()['rows'][0]['elements'][i]['distance']['text'].split()[0]
#         i += 1
#     dict = sorted(dict.items(),key=lambda x: x[1]['distance_from_origin'])
#     return dict

# def farthest_destination(list):
#     lat_long = []
#     # lat and long for the farthest place
#     for param in list[-1]:
#         if 'latitude' in param:
#             lat_long.append(param['latitude'])
#         if 'longitude' in param:
#             lat_long.append(param['longitude'])
#     return lat_long

# def waypoints(list):
#     print(list)
#     i = 0
#     for item in list:
#         i += 1
#         for param in item:
#             if 'place_id' in param:
#                 place_id = param['place_id']
#                 if len(list) == i:
#                     all_id = place_id
#                 else:
#                     all_id = place_id + "|"
#     print(all_id)
#     return all_id

# def farthest_destination():
#     lat_long = []
#     conn = psycopg2.connect(DATABASE_URL)
#     cur = conn.cursor()
#     cur.execute("""
#     SELECT latitude,longitude FROM stores_1 WHERE
#     distance_from_origin=(SELECT MAX(distance_from_origin) FROM stores_1)
#     """)
#     result = cur.fetchone()
#     lat_long.append(result[0])
#     lat_long.append(result[1])
#     cur.close()
#     return lat_long

def all_ids():
    waypoints_string = ""
    ids = []
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT place_id FROM stores_1 ORDER BY distance_from_origin DESC
    """)
    results = cur.fetchall()
    cur.close()
    for row in results:
        ids.append(row[0])
    while ids:
        if len(ids) != 1:
            waypoints_string = waypoints_string + f"place_id:{ids.pop()}|"
        elif len(ids) == 1:
            waypoints_string = waypoints_string + f"place_id:{ids.pop()}"
    return waypoints_string

def geocode_address(address):
    lat_long = []
    address = address.replace(' ','%20')
    address = address.replace('/','%2F')
    address = address.replace(',','%2C')
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.request("GET",url,headers=headers,data=payload)
    lat_long.append(response.json()['results'][0]['geometry']['location']['lat'])
    lat_long.append(response.json()['results'][0]['geometry']['location']['lng'])
    return lat_long

def hash(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

def check_password(password,hashed_password):
    return bcrypt.checkpw(password.encode(),hashed_password.encode())

def create_user_on_db(first_name,email,password,lat,long):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO users(first_name,email,password,latitude,longitude) VALUES(%s,%s,%s,%s,%s)
    """,(first_name,email,password,lat,long))
    conn.commit()
    cur.close()

def check_email_db(email):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT COUNT(*) FROM users WHERE email = %s
    """,(email,))
    matched_users = cur.fetchall()[0][0]
    if matched_users == 1:
        return True
    else:
        return False

def check_login_details(email,password):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT password FROM users WHERE email=%s
    """,(email,))
    hashed_password = cur.fetchall()[0][0]
    cur.close()
    if check_password(password,hashed_password):
        return True
    else:
        return False
    
def retrieve_userID(email):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT id FROM users WHERE email=%s
    """,(email,))
    user_id = cur.fetchall()[0][0]
    return user_id

def retrieve_stores(userID):
    stores = []
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT id,store_name,location FROM stores_1 WHERE user_id=%s
    """,(userID,))
    results = cur.fetchall()
    if cur.rowcount != 0:
        for row in results:
            stores.append({
                'id':row[0],
                'store':row[1].split(' ')[0],
                'location':row[2]
            })
    cur.close()
    return stores

def store_items(user_id,store_id,item):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT id FROM items WHERE user_id=%s AND store_id=%s
    """,(user_id,store_id))
    if cur.rowcount != 0:
        items_table_id = cur.fetchall()[0][0]
        cur.execute("""
        SELECT item_list FROM items WHERE user_id=%s AND store_id=%s
        """,(user_id,store_id))
        items = cur.fetchall()[0][0]
        items = items + "," + item
        cur.execute("""
        UPDATE items SET item_list=%s WHERE id=%s
        """,(items,items_table_id))
        conn.commit()
    else:
        cur.execute("""
        INSERT INTO items(user_id,store_id,item_list) VALUES(%s,%s,%s)
        """,(user_id,store_id,item))
        conn.commit()
    cur.close()

def retrieve_items(user_id,store_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT item_list FROM items WHERE user_id=%s AND store_id=%s
    """,(user_id,store_id))
    if cur.rowcount != 0:
        items = cur.fetchall()[0][0]
    else:
        items = None
    cur.close()
    return items

def retrieve_address(email):
    lat_long = []
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT latitude,longitude FROM users WHERE email=%s
    """,(email,))
    results = cur.fetchall()
    lat = results[0][0]
    long = results[0][1]
    cur.close()
    lat_long.append(lat)
    lat_long.append(long)
    return lat_long
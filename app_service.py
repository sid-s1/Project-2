import requests, os, psycopg2, bcrypt
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('api_key')

DATABASE_URL = os.environ.get('DATABASE_URL','dbname=shopping_list')
payload={}
headers = {}
place_id_dict = {}

def store_search_json(store,email):
    user_address = retrieve_address(email)
    lat = user_address[0]
    long = user_address[1]
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={store}&location={lat}%2C{long}&radius=10000000&key={api_key}"
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def get_place_id(response):
    if len(response['predictions']) > 0:
        return response['predictions'][0]['place_id']

def get_store_name(response):
    if len(response['predictions']) > 0:
        return response['predictions'][0]['structured_formatting']['main_text'] + "," + response['predictions'][0]['structured_formatting']['secondary_text']

def store_place_details(place_id,store_name,user_id):
    if check_store_exists(user_id,store_name) != 'exists':
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
    else:
        return 'exists'

def all_placeids_for_maps(user_id):
    waypoints_string = ""
    ids = []
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT place_id FROM stores_1 WHERE user_id=%s ORDER BY distance_from_origin DESC
    """,(user_id,))
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
    if check_email_db(email):
        return 'exists'
    else:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO users(first_name,email,password,latitude,longitude) VALUES(%s,%s,%s,%s,%s)
        """,(first_name,email,password,lat,long))
        conn.commit()
        cur.close()

def is_valid_email(email):
    if email.rfind('.') + 1 < len(email) and email[email.rfind('.') + 1] != '.' and email.count('@') == 1 and email.find('@') - 1 >= 0 and email[email.find('@') - 1] != '.' and email.find('.', email.find('@'), len(email) - 1) >= email.find('@') + 2:
        return True
    else:
        return False

def check_email_db(email):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT COUNT(*) FROM users WHERE email = %s
    """,(email,))
    matched_users = cur.fetchall()[0][0]
    cur.close()
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

def retrieve_userName(email):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT first_name FROM users WHERE email=%s
    """,(email,))
    user_name = cur.fetchall()[0][0]
    return user_name

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

def check_store_exists(user_id,store_to_add):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM stores_1 WHERE user_id=%s AND store_name=%s
    """,(user_id,store_to_add))
    if cur.rowcount != 0:
        return 'exists'

def check_item_exists(item_to_add,string):
    items = string.split(',')
    for item in items:
        print(item)
        if item.lower() == item_to_add.lower():
            return True
    return False


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
        if check_item_exists(item,items) == False:
            items = items + "," + item
            cur.execute("""
            UPDATE items SET item_list=%s WHERE id=%s
            """,(items,items_table_id))
            conn.commit()
            return 'success'
    else:
        cur.execute("""
        INSERT INTO items(user_id,store_id,item_list) VALUES(%s,%s,%s)
        """,(user_id,store_id,item))
        conn.commit()
        return 'success'
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

def retrieve_stores_items(email):
    items_by_store = []
    user_id = retrieve_userID(email)
    stores = retrieve_stores(user_id)
    for store in stores:
        items = retrieve_items(user_id,store['id'])
        items_by_store.append({
            'id':store['id'],
            'store':store['store'],
            'location':store['location'],
            'item_list':items
        })
    return items_by_store

def edit_item(user_id,store_id,old_item_name,new_item_name):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    current_items_string = retrieve_items(user_id,store_id)
    current_items_array = current_items_string.split(',')
    for index in range(len(current_items_array)):
        if current_items_array[index].lower() == old_item_name.lower():
            current_items_array[index] = new_item_name
    new_items_string = (',').join(current_items_array)
    cur.execute("""
    UPDATE items SET item_list=%s WHERE user_id=%s AND store_id=%s
    """,(new_items_string,user_id,store_id))
    conn.commit()
    cur.close()

def delete_item(user_id,store_id,item_to_delete):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    current_items_string = retrieve_items(user_id,store_id)
    current_items_array = current_items_string.split(',')
    for item in current_items_array:
        if item.lower() == item_to_delete.lower():
            current_items_array.pop(current_items_array.index(item))
    new_items_string = (',').join(current_items_array)
    cur.execute("""
    UPDATE items SET item_list=%s WHERE user_id=%s AND store_id=%s
    """,(new_items_string,user_id,store_id))
    conn.commit()
    cur.close()

def delete_store(user_id,store_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM items WHERE user_id=%s AND store_id=%s
    """,(user_id,store_id))
    conn.commit()
    cur.execute("""
    DELETE FROM stores_1 WHERE user_id=%s AND id=%s
    """,(user_id,store_id))
    conn.commit()
    cur.close()
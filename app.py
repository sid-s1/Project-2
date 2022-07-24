from flask import Flask, redirect, request, render_template, session
import requests, os, psycopg2
import app_service

# key_from_file = open('sec_key.txt','r').read()
SECRET_KEY = os.environ.get('SECRET_KEY','sidisgr8')
store_list = []
item_list = {}

app = Flask('__name__')
app.config['SECRET_KEY'] = SECRET_KEY
api_key = open('maps.txt','r').read()

@app.route('/')
def index():
    return render_template('index.html',user=session.get('email'))

@app.route('/list')
def shopping_list():
    items_by_store = []
    if session.get('email') != None:
        user_id = app_service.retrieve_userID(session.get('email'))
        stores = app_service.retrieve_stores(user_id)
        for store in stores:
            items = app_service.retrieve_items(user_id,store['id'])
            items_by_store.append({
                'id':store['id'],
                'store':store['store'],
                'location':store['location'],
                'item_list':items
            })
        return render_template('shopping.html',key=api_key,user=session.get('email'),stores=items_by_store)

# based on distance between origin and each destination/waypoint, create a sorted list of place_id's and use that to create a route then

# use places details api google and use place_id to show some details to user in html so they can choose, then once they choose through another form perhaps make it pin drop on maps with route from their home

@app.route('/list',methods=["POST"])
def shopping_list_search():
    searched_store = request.form.get('searched-store')
    user_id = app_service.retrieve_userID(session.get('email'))

    store_search_json = app_service.store_search_json(searched_store)
    place_id = app_service.get_place_id(store_search_json)
    store_name = app_service.get_store_name(store_search_json)

    app_service.store_place_details(place_id,store_name,user_id)

    # cancel from here
    # stores_dict = app_service.store_place_details(place_id,store_name)
    # all_store_info_list = app_service.all_store_distances(stores_dict)
    
    # latitude = app_service.farthest_destination(all_store_info_list)[0]
    # longitude = app_service.farthest_destination(all_store_info_list)[1]
    # all_ids = app_service.waypoints(all_store_info_list)
    return redirect('/list')


@app.route('/display')
def list_route_display():
    # lat_long_farthest = app_service.farthest_destination()
    # lat = lat_long_farthest[0]
    # long = lat_long_farthest[1]
    if session.get('email') != None:
        all_ids = app_service.all_ids()
        lat_long = app_service.retrieve_address(session.get('email'))
        return render_template('route.html',key=api_key,ids=all_ids,user=session.get('email'),lat=lat_long[0],long=lat_long[1])

@app.route('/signup')
def signup_page():
    if session.get('email') == None:
        return render_template('signup_page.html',key=api_key,user=session.get('email'))

@app.route('/signup',methods=["POST"])
def signup_process():
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    password = request.form.get('entered_password')
    address = request.form.get('home')

    hashed_password = app_service.hash(password)
    geocoded_address = app_service.geocode_address(address)
    home_latitude = geocoded_address[0]
    home_longitude = geocoded_address[1]
    app_service.create_user_on_db(first_name,email,hashed_password,home_latitude,home_longitude)
    return redirect('/')

@app.route('/login')
def login_page():
    if session.get('email') == None:
        return render_template('login_page.html',user=session.get('email'))

@app.route('/login',methods=["POST"])
def login_check():
    email = request.form.get('email')
    password = request.form.get('entered_password')
    if app_service.check_email_db(email):
        if app_service.check_login_details(email,password):
            session['email'] = email
            return redirect('/')
        else:
            return render_template('login_page.html',unmatched=True)
    else:
        return render_template('login_page.html',no_email=True)

@app.route('/logout_check')
def logout_decision():
    if session.get('email') != None:
        return render_template('logout_decision.html',user=session.get('email'))

@app.route('/logout',methods=["POST"])
def logout():
    action = request.form.get('action')
    if action == 'Yes please':
        session.pop('email')
    else:
        print('no')
    return redirect('/')

@app.route('/add_item',methods=["POST"])
def add_item_action():
    store_id = request.form.get('store-id')
    added_item = request.form.get('added-item')
    user_id = app_service.retrieve_userID(session.get('email'))
    app_service.store_items(user_id,store_id,added_item)
    return redirect('/list')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, request, render_template, session
import os
import app_service
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('api_key')

SECRET_KEY = os.environ.get('SECRET_KEY','sidisgr8')
store_list = []
item_list = {}

app = Flask('__name__')
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    email = session.get('email')
    if session.get('email') != None:
        stores_and_items = app_service.retrieve_stores_items(email)
        user_id = app_service.retrieve_userID(email)
        lat_long = app_service.retrieve_address(email)
        all_placeids_for_maps = app_service.all_placeids_for_maps(user_id)
        return render_template('homepage.html',key=api_key,ids=all_placeids_for_maps,user=session.get('email'),lat=lat_long[0],long=lat_long[1],stores=stores_and_items,user_id=user_id)
    else:
        return render_template('homepage.html',user=session.get('email'),key=api_key)

@app.route('/',methods=["POST"])
def list_route_action():
    email = session.get('email')
    if session.get('email') != None and request.form.get('delete_item_name') == None and request.form.get('delete_store') == None:
        user_id = app_service.retrieve_userID(email)
        store_id = request.form.get('store_id')
        old_item_name = request.form.get('old_item_name')
        new_item_name = request.form.get('new_item_name')
        app_service.edit_item(user_id,store_id,old_item_name,new_item_name)
    elif session.get('email') != None and request.form.get('delete_item_name') != None:
        user_id = app_service.retrieve_userID(email)
        store_id = request.form.get('delete_item_store')
        item_to_delete = request.form.get('delete_item_name')
        app_service.delete_item(user_id,store_id,item_to_delete)
    elif session.get('email') != None and request.form.get('delete_store') != None:
        user_id = app_service.retrieve_userID(email)
        store_id = request.form.get('delete_store')
        app_service.delete_store(user_id,store_id)
    return redirect('/')

@app.route('/list')
def shopping_list():
    email = session.get('email')
    if session.get('email') != None:
        stores_and_items = app_service.retrieve_stores_items(email)
        return render_template('shopping.html',key=api_key,user=session.get('email'),stores=stores_and_items)

@app.route('/list',methods=["POST"])
def shopping_list_search():
    searched_store = request.form.get('searched-store')
    user_id = app_service.retrieve_userID(session.get('email'))

    store_search_json = app_service.store_search_json(searched_store)
    place_id = app_service.get_place_id(store_search_json)
    store_name = app_service.get_store_name(store_search_json)

    if app_service.check_store_exists(user_id,store_name) != 'exists':
        app_service.store_place_details(place_id,store_name,user_id)
        return redirect('/list')
    else:
        return render_template('entity_exists.html',entity='store')


@app.route('/display')
def list_route_display():
    email = session.get('email')
    if session.get('email') != None:
        stores_and_items = app_service.retrieve_stores_items(email)
        user_id = app_service.retrieve_userID(email)
        lat_long = app_service.retrieve_address(email)
        all_placeids_for_maps = app_service.all_placeids_for_maps(user_id)
        return render_template('route.html',key=api_key,ids=all_placeids_for_maps,user=session.get('email'),lat=lat_long[0],long=lat_long[1],stores=stores_and_items,user_id=user_id)

@app.route('/signup')
def signup_page():
    if session.get('email') == None:
        return render_template('signup_page.html',key=api_key,user=session.get('email'),invalid_email=False)

@app.route('/signup',methods=["POST"])
def signup_process():
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    password = request.form.get('entered_password')
    address = request.form.get('home')
    if app_service.is_valid_email(email):
        if app_service.check_email_db(email) == False:
            hashed_password = app_service.hash(password)
            geocoded_address = app_service.geocode_address(address)
            home_latitude = geocoded_address[0]
            home_longitude = geocoded_address[1]
            app_service.create_user_on_db(first_name,email,hashed_password,home_latitude,home_longitude)
            return redirect('/login')
        else:
            return render_template('entity_exists.html',entity='email')
    else:
        return render_template('signup_page.html',key=api_key,user=session.get('email'),invalid_email=True)

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

@app.route('/edit_item')
def trial():
    return render_template('trial.html')

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
    store_id = request.form.get('selected-store')
    added_item = request.form.get('added-item')
    user_id = app_service.retrieve_userID(session.get('email'))
    if app_service.store_items(user_id,store_id,added_item) != 'exists' and app_service.store_items(user_id,store_id,added_item) != None:
        return redirect('/list')
    else:
        return render_template('entity_exists.html',entity='item')

if __name__ == '__main__':
    app.run(debug=True)

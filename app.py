from flask import Flask, redirect, request, render_template
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
    return render_template('index.html')

@app.route('/list')
def shopping_list():
    return render_template('shopping.html',key=api_key)

# based on distance between origin and each destination/waypoint, create a sorted list of place_id's and use that to create a route then

# use places details api google and use place_id to show some details to user in html so they can choose, then once they choose through another form perhaps make it pin drop on maps with route from their home

@app.route('/list',methods=["POST"])
def shopping_list_search():
    searched_store = request.form.get('searched-store')

    store_search_json = app_service.store_search_json(searched_store)
    place_id = app_service.get_place_id(store_search_json)
    store_name = app_service.get_store_name(store_search_json)

    app_service.store_place_details(place_id,store_name)

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
    all_ids = app_service.all_ids()
    return render_template('route.html',key=api_key,ids=all_ids)


if __name__ == '__main__':
    app.run(debug=True)

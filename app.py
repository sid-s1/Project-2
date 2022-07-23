from flask import Flask, request, render_template
import requests, os, psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL','dbname=shopping_list')
key_from_file = open('sec_key.txt','r').read()
SECRET_KEY = os.environ.get('SECRET_KEY',key_from_file)

app = Flask('__name__')
app.secret_key = SECRET_KEY.encode()
api_key = open('maps.txt','r').read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def shopping_list():
    return render_template('shopping.html',key=api_key)

@app.route('/list',methods=["POST"])
def shopping_list_search():
    searched_store = request.form.get('searched-store')
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={searched_store}&types=supermarket&location=-33.814999%2C151.001114&radius=10000&strictbounds=true&key={api_key}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # use places details api google and use place_id to show some details to user in html so they can choose, then once they choose through another form perhaps make it pin drop on maps with route from their home
    print(response.text)
    return render_template('shopping.html',key=api_key)


@app.route('/display')
def list_route_display():
    return render_template('route.html',key=api_key)


if __name__ == '__main__':
    app.run(debug=True)

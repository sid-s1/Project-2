![Shopping List | Route Generator](https://github.com/sid-s1/Project-2/blob/main/static/images/banner.png?raw=true)

## Web-App that allows you to
- Add stores near your home to your Shopping List
- Add different items to each of those stores
- See a driving route 
  - From your home 
  - Going through each store (only with added items for ease) 
  - Back to home

## Use App

https://radiant-retreat-54789.herokuapp.com/

## Technologies Used
1. HTML
2. CSS
3. Javascript
4. Python
5. Flask
6. PostgreSQL

## Dependencies for Python
1. flask
2. psycopg2
3. bcrypt
4. gunicorn
5. requests
6. python-dotenv

## Installation Directions
1. All dependencies are noted in the "requirements.txt" file
2. Install all dependencies by going to project folder on your terminal and typing: 
   - `python3 -r requirements.txt`

## APIs

1. **Google Autocomplete**: To predict search results based on what the user is typing
2. **Google Geocoding**: To get latitude and longitude based on location (home) address
3. **Google Details**: To get latitude and longitude based on place ID of selected store
4. **Google Directions**: To get routing map from home address back to based, with waypoints set as each store

## Configuration Directions
1. In your project folder, create file ".env"
2. In the format below, write down your Google api key and a secret key for cookie storage (length of your choice)
   - `api_key="xxyyzzaabbcc"`
   - `SECRET_KEY="abcabcabcabcabcaabcabcabcabcabca"`
3. If you want to generate a random 16 or 32 digit key using python, type the following into your terminal:
   - `python3`
   - `import secrets`
   - `secrets.token_hex(32)`
4. Create database on your local machine:
   - `psql postgres`
   - `CREATE DATABASE my_db`
5. Set up the database on your local machine using the provided "schema.sql" file:
   - `psql my_db < sampleProjectFolder/schema.sql`
6. Create a virtual environment. Go to your project folder and then:
   - `python3 -m venv venv`
7. To start your virtual environment:
   - `source venv/bin/activate`
8. To run app on your local machine:
   - `python3 app.py`
9. Based on the default port you've set, you will be able to view the app. For me, I had to enter the following in my browser:
    - `localhost:5000`
   
## Database Design

The database consists of three tables:
1. Users
   - Captures the first name, email and (protected) password of the user
   - The user-inputted home address in the sign-up form gets converted to latitude and longitude of user's home address (Google Geocoding API)
   - The 'secret' column holds the value of the user's answer to their secret question
2. Stores
   - Captures the store name and user id of the user who added that store to their shopping list
   - Code uses Google Places API and Geocoding API and stores place id, latitude, longitude, location (suburb) and distance from user's home address
3. Items
   - Stores user id for user who is adding the items
   - User can only add items after a store is added, so stores store id as well
   - Stores all items for that store + user pair separated by a comma in item_list

![ERD](https://github.com/sid-s1/Project-2/blob/main/static/images/ERD.jpg?raw=true)

## Future Work

1. Modal box shows up that says "Thanks for signing up, go login now"
2. Javascript prompt for "No commas please" as user adds items to their list
3. Option to add quantity of each item in the list
4. Management of quantity of each item for each store on the homepage
5. Improve DB design (nullifying future work Point 2) so as to:
   - Remove repetition of stores - multiple users might add the same store to their shopping list even if their list of items is different
   - Better parsing and storing of items so as to remove the "comma" problem
6. Media Queries for use on mobile devices
7. Adding a "forgot my password" section to login page &#10004;
8. Restricting users to only use real email addresses
9. Sending account confirmation emails to users and sending real password reset emails
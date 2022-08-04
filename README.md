# Shopping List | Route Generator

A web-app that allows you to add stores to your shopping list using Google Search API; you can then add items to each store; as you do that, this app will also create a route starting from your home address (that you used during sign-up) and add all the stores as waypoints returning back to home.

## Link

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

## APIs

1. **Google Autocomplete**: To predict search results based on what the user is typing
2. **Google Geocoding**: To get latitude and longitude based on location (home) address
3. **Google Details**: To get latitude and longitude based on place ID of selected store
4. **Google Directions**: To get routing map from home address back to based, with waypoints set as each store

Step by step as to what happens from the signup page through to the end?
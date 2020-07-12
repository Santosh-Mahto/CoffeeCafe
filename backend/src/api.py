import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
     response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
     response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,PATCH,DELETE,OPTIONS')
     return response
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    
    if drinks:
        return jsonify({
                       'success' : True,
                       'drinks' : [drink.short() for drink in drinks] 
                       })
    else:
        abort(404)

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-details')
def get_drink_details(jwt):
    drinks = Drink.query.order_by(Drink.id).all()
    
    if drinks:
        return jsonify({
                       'success' : True,
                       'drinks' : [drink.long() for drink in drinks] 
                       })
    

'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(jwt):
    data = request.get_json()
    if 'title' and 'recipe' not in data:
        abort(422)

    title = data['title']
    recipe = json.dumps(data['recipe'])
    drink = Drink(title = title, recipe = recipe)
    drink.insert()

    return jsonify({
                    'success' : True,
                    'drinks' : [drink.long()]
                   })    

'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, id):
    drink = Drink.query.get(id)
    if drink is None:
        abort(404)

    data = request.get_json()
    if 'title' in data:
        drink.title = data['title']

    if 'recipe' in data:
        drink.recipe = json.dumps(data['recipe'])

    drink.update()

    return jsonify({
                    'success' : True,
                    'drinks' : [drink.long()]
                    })           

'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt,id):
    drink = Drink.query.get(id)

    if drink is None:
        abort(404)

    drink.delete()
    return jsonify({
                   "success" : True,
                   "delete" : drink.id
    })    


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def unauthorize(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                   'success' : False,
                   'error' : error.status_code,
                   'message' : error.error['description'] 
                   })                    
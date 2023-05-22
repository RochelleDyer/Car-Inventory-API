from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, Car, car_schema, cars_Schema
from models import db, Contact, contact_schema, contacts_Schema

api = Blueprint( 'api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'test': 'data'}

# Create Car
@api.route('/cars',methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    description = request.json['description']
    user_token = current_user_token.token

    car = Car (make, model, year, description, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_Schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify ({'message': 'Invalid token'}), 401


# Update endpoint
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json ['year']
    car.description = request.json ['description']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
    
# Delete endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    print (car)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
# example
# from werkzeug.exceptions import NotFound

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        for attr in request.get_json():
            # print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            # print(request.get_json().get(attr))
            setattr(plant, attr, request.get_json().get(attr))
        
        # for attr in request.form:
        #     print(request.form[attr])
        #     setattr(plant, attr, request.form[attr])   
            
        db.session.add(plant)
        db.session.commit()
        
        response_dict = plant.to_dict()
        
        response = make_response(jsonify(response_dict), 200)
        return response
    
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        
        db.session.delete(plant)
        db.session.commit()
        
        return make_response("", 204)


api.add_resource(PlantByID, '/plants/<int:id>')

# @app.errorhandler(404)
# def handle_not_found(e):
    
#     response = make_response(
#         "Not Found: The requested resource does not exist.",
#         404
#     )

#     return response

# app.register_error_handler(404, handle_not_found)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

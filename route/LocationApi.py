from flask import request, jsonify, Blueprint
from flask_restful import Api, Resource
from models.Location import Location
from schema.LocationSchema import LocationSchema
from infrastructure.database import db_session

deleteAllLocationsRoute = Blueprint('deleteAll', __name__)
location_bp = Blueprint('location_api', __name__)
api = Api(location_bp)

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

# todo: terminar el crud de locations
class LocationResource(Resource):

    def get(self):
        locations = Location.query.all()
        response = locations_schema.dump(locations)
        return response

    def post(self):
        name = request.json['name']
        lat = request.json['lat']
        lng = request.json['lng']

        location = Location(name=name, lat=lat, lng=lng)
        db_session.add(location)
        db_session.commit()
        return location_schema.jsonify(location), 201

    def delete(self, id):
        # todo: arreglar
        location = Location.query.get(id)
        db_session.delete(location)
        db_session.commit()
        return location_schema.jsonify(location), 204


api.add_resource(LocationResource, '/locations', '/locations/<int:id>', '/locations')


@deleteAllLocationsRoute.route('/delete/all')
def delete_all():
    db_session.query(Location).delete()
    db_session.commit()
    return jsonify({"message": "All locations has been eliminated"}), 204

from flask import request, jsonify, Blueprint
from flask_restful import Api, Resource

from infrastructure.database import db_session
from models.Location import Location
from schema.LocationSchema import LocationSchema

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
        try:
            location = Location.query.where(Location.id == id).first()
            print("location: " + str(location))
            db_session.delete(location)
            db_session.commit()
            return {'message': 'Location deleted'}, 204
        except Exception as e:
            return {'message': str(e)}, 404

    def put(self, id):
        # update location
        location = Location.query.where(Location.id == id).first()

        if location:
            location.name = request.json['name']
            location.lat = request.json['lat']
            location.lng = request.json['lng']

            db_session.commit()
            return {'message': 'Location updated'}, 200
        else:
            return {'message': 'Location not found'}, 404


api.add_resource(LocationResource, '/locations', '/locations/<int:id>', '/locations/<int:id>', '/locations/<int:id>')


@deleteAllLocationsRoute.route('/locations/delete/all')
def delete_all():
    db_session.query(Location).delete()
    db_session.commit()
    return jsonify({"message": "All locations has been eliminated"}), 204

from infrastructure.ma import ma
from marshmallow.fields import Str, Number, Float


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "lng", "lat"]

    id = Number()
    name = Str()
    lng = Float()
    lat = Float()

from sqlalchemy import Column, Integer, String, Float
from infrastructure.database import Base


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

    def coordinates(self):
        return self.lat, self.lng

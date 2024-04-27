from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    timeCreated = db.Column(db.DateTime)

    role = db.Column(db.String(80), unique=False, nullable=False)

    sessions = relationship('Session', backref='user')
    logs = relationship('Log', backref='user')
    alerts = relationship('Alert', backref='user')
    access_token = db.Column(db.String(1024))

class Session(db.Model):
    __tablename__ = 'sessions'
    sessionID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    timeCreated = db.Column(db.DateTime)
    timeEnded = db.Column(db.DateTime)

    logs = relationship('Log', backref='session')
    alerts = relationship('Alert', backref='session')

class Log(db.Model):
    __tablename__ = 'logs'
    logID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    xCoor = db.Column(db.Integer)
    yCoor = db.Column(db.Integer)

    sessionID = db.Column(db.Integer, db.ForeignKey('sessions.sessionID'))

class Alert(db.Model):
    __tablename__ = 'alerts'
    alertID = db.Column(db.Integer, primary_key=True)
    sessionID = db.Column(db.Integer, db.ForeignKey('sessions.sessionID'))
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    type = db.Column(Enum('TYPE_1', 'TYPE_2', name='alert_types'))
    timeCreated = db.Column(db.DateTime)


class RackLocation(db.Model):
    __tablename__ = 'rack_locations'
    rackID = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    location_x = db.Column(db.String(100), nullable=False)
    location_y = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    @staticmethod
    def preload_data():
        try:
            # Clear existing data
            db.session.query(RackLocation).delete()
            db.session.commit()

            # Insert new data
            rack_locations_data = [
                {"rackID": 1, "location_name": "Red River Meeting Room", "location_x": "49.892086", "location_y": "-97.137574", "description": "Convenient location for business meetings with a view of the Red River."},
                {"rackID": 2, "location_name": "City Center Storage", "location_x": "49.895078", "location_y": "-97.142578", "description": "Central spot for easy access to downtown attractions and shopping districts."},
                {"rackID": 3, "location_name": "Downtown Hub", "location_x": "49.887623", "location_y": "-97.145937", "description": "Located in the heart of downtown Winnipeg, adjacent to public transportation hubs."},
                {"rackID": 4, "location_name": "Skyline Depot", "location_x": "49.888732", "location_y": "-97.131207", "description": "Ideal location for commuters, surrounded by cafes and restaurants."},
                {"rackID": 5, "location_name": "Commerce Corner Rack", "location_x": "49.893541", "location_y": "-97.136942", "description": "Central location near popular shopping districts, perfect for retail storage."},
                {"rackID": 6, "location_name": "Metro Meeting Room", "location_x": "49.888186", "location_y": "-97.139785", "description": "Near downtown attractions and entertainment venues, ideal for business meetings."},
                {"rackID": 7, "location_name": "Plaza Point Storage", "location_x": "49.891247", "location_y": "-97.140398", "description": "Located in a bustling commercial area, with easy access to public amenities."},
                {"rackID": 8, "location_name": "Urban Junction Rack", "location_x": "49.890623", "location_y": "-97.134557", "description": "Convenient location for commuters, with access to major thoroughfares."},
                {"rackID": 9, "location_name": "Gateway Rack", "location_x": "49.886275", "location_y": "-97.135887", "description": "Close to downtown attractions and transportation hubs, with a view of the city skyline."},
                {"rackID": 10, "location_name": "Riverfront Storage", "location_x": "49.891754", "location_y": "-97.132946", "description": "Prime location near the riverfront, offering scenic views and easy access to downtown amenities."}
            ]

            for data in rack_locations_data:
                new_location = RackLocation(**data)
                db.session.add(new_location)
            db.session.commit()

            return {"message": "Data preloaded successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
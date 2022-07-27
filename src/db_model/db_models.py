from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from src.common import DT_FMT

db = SQLAlchemy()


class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30), nullable=False)
    make = db.Column(db.String(30), nullable=False)
    slots = db.relationship('Schedule', backref='bus', lazy='select')

    def __repr__(self) -> str:
        return '{self.make}:{self.model}@{self.driver}'

    def as_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'make': self.make,
        }


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    social_security_number = db.Column(db.Integer, unique=True, nullable=False)
    shifts = db.relationship('Schedule', backref='driver', lazy='select')

    def __repr__(self) -> str:
        return '{self.first_name} {self.last_name}'

    def as_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    dt_start = db.Column(db.DateTime, nullable=False)
    dt_end = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return '{self.driver}@{self.bus_id} {self.dt_start} - {self.dt_end}'

    def as_dict(self):
        return {
            'id': self.id,
            'driver_id': f'{self.driver_id}',
            'bus_id': self.bus_id,
            'dt_start': datetime.strftime(self.dt_start, DT_FMT),
            'dt_end': datetime.strftime(self.dt_end, DT_FMT)
        }

    def driver_is_free_at(driver_id: int, dt_start: datetime, dt_end: datetime) -> bool:
        return True

    def bus_is_free_at(bus_id: int, dt_start: datetime, dt_end: datetime) -> bool:
        return True


if __name__ == '__main__':
    # * this will run only if the docker mySQL container doesn't detect a volume
    db.create_all()

# Author: Joshua Ferguson

# WIP - Not yet implemented For the Date, Time, and TimeZone Models
# TODO: Integrate into the Corresponding Models
# TODO: Validate the Date, Time, and TimeZone Fields in their Schema

import datetime

from sqlalchemy.orm import validates

from Backend.src.extensions import db, ma  # DB and Marshmallow Instances
from Backend.src.validators import validators  # Custom Validators

# ---- Date ----


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary Key

    # ---Dimensional Fields---
    date = db.Column(datetime.date, nullable=False)


class DateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Date
        load_instance = True
        include_relationships = True


# ---- Time ----


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    time = db.Column(datetime.time, nullable=False)


class TimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Time
        load_instance = True
        include_relationships = True


# ---- Time Zone ----


class TimeZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    time_zone = db.Column(db.String(500), nullable=False)


class TimeZoneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TimeZone
        load_instance = True
        include_relationships = True

    @validates("time_zone")
    def validate_time_zone(self, time_zone):
        # Length and Profanity Filter
        validators.val_length(time_zone, upper_bound=500)

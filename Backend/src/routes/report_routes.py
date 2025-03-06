# Author: Joshua Ferguson

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas

# Blueprint for the Message Routes
report_bp = Blueprint('report_bp', __name__)

report_bp_schema = models.report.ReportSchema()


@report_bp.route('/users/reports', methods=['POST'])
def post_user_report():
    return

@report_bp.route('/users/reports', methods=['GET'])
def get_user_report():
    return
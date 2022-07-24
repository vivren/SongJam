from flask import Blueprint

roomBP = Blueprint('room', __name__)

from . import room

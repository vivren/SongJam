from flask import Blueprint
from .classes import Rooms

roomActionBP = Blueprint('roomAction', __name__)
rooms = Rooms()

from . import roomAction

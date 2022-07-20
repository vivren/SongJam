from flask import Blueprint

roomAction = Blueprint('roomAction', __name__)

from . import roomAction

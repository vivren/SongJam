from flask import Blueprint

roomActionBP = Blueprint('roomAction', __name__)

from . import roomAction

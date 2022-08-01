from flask import Blueprint
from .classes import Playlist

roomBP = Blueprint('room', __name__)
playlist = Playlist()

from . import room, events

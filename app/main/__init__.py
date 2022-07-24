from flask import Blueprint

mainBP = Blueprint('main', __name__)

from . import main

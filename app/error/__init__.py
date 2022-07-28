from flask import Blueprint

errorBP = Blueprint('error', __name__)

from . import error

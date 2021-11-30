from flask import Blueprint

auth_blue = Blueprint('auth',__name__)

from . import views,forms
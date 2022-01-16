from flask import Blueprint

admin_blue_1 = Blueprint('admin_1',__name__)

from . import views,forms,modelViews
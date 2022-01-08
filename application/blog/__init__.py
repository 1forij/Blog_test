from flask import Blueprint

blog_blue = Blueprint('blog',__name__)

from . import views,forms
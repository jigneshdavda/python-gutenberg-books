from flask import Blueprint
from app.controller.admin.BookController import BookController

guternberg_api = Blueprint('guternberg_api', __name__,url_prefix='/api')

guternberg_api.add_url_rule('/books',view_func=BookController().login, methods=['POST'])
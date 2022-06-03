from urllib import response
from app.constants import *
from app.model.BookModel import BookModel
from app.services.helper import failureResponse, successResponse
from http import HTTPStatus
from flask import request
from flask_sieve import Validator

class BookController(BookModel):
    
    def __init__(self):
        super().__init__()
    
    def login(self):
        
        # Setup a form request in local variable
        formRequest = request.form
        
        # Setup validation rules
        rules = {
            'limit': ['required', 'integer', 'max:25']
        }
        
        # Send rules and request to validator
        validator = Validator(rules=rules,request=formRequest)
        
        # Check whether validator passes all rules
        if validator.passes():
            
            # Create below list for output
            
            """
            Title of the book
            Information about the author
            Genre
            Language
            Subject(s)
            Bookshelf(s)
            A list of links to download the book in the available formats (mime-types)
            """
            # Query to book filter function to get books data
            bookResult = BookModel().get_books_by_filter(formRequest)
            
            # Check bookResult
            if bookResult:
                return successResponse(BOOKS_SUCCESSFULL_LISTED, bookResult, HTTPStatus.OK)
            else:
                return successResponse(NO_SEARCH_RESULT_FOUND, bookResult, HTTPStatus.OK)
        
        # Send failure response
        return failureResponse(ONE_OR_MORE_PARAMETERS_MISSING, validator.messages(), HTTPStatus.OK)
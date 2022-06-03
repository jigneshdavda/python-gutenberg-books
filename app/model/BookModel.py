from ast import Str
from unittest import result
from app import mysql

class BookModel():
    def __init__(self):
        try:
            self.conn = mysql.connection.cursor()
            print('Database Connected')
        except:
            print('Database connection problem')
            
    def get_books_by_filter(self, formData):
        
        
        
        return self.get_book_info(3, formData['limit'])
    
    def get_author_info(self, bookId):
        authorQuery = "SELECT name, birth_year, death_year FROM `books_book_authors` as bba, `books_author` as ba WHERE bba.author_id = ba.id AND book_id = "+str(bookId)
        self.conn.execute(authorQuery)
        authorResults = self.conn.fetchall()
        return authorResults
    
    def get_genre_info(self, bookId):
        genreQuery = "SELECT * FROM books_book limit 10"
        self.conn.execute(genreQuery)
        genreResults = self.conn.fetchall()
        return genreResults
    
    def get_language_info(self, bookId):
        languageQuery = "SELECT bl.id as id, code FROM `books_book_languages` as bbl, `books_language` as bl WHERE bbl.language_id = bl.id AND bbl.book_id = "+str(bookId)
        self.conn.execute(languageQuery)
        languageResults = self.conn.fetchall()
        return languageResults
    
    def get_subjects_info(self, bookId):
        subjectsQuery = "SELECT bs.id as id, name FROM `books_book_subjects` as bbs, `books_subject` as bs WHERE bbs.subject_id = bs.id AND bbs.book_id = "+str(bookId)
        self.conn.execute(subjectsQuery)
        subjectsResults = self.conn.fetchall()
        return subjectsResults
    
    def get_book_shelfs_info(self, bookId):
        book_shelfsQuery = "SELECT bb.id as id, name FROM `books_book_bookshelves` as bbb, `books_bookshelf` as bb WHERE bbb.bookshelf_id = bb.id AND bbb.book_id = "+str(bookId)
        self.conn.execute(book_shelfsQuery)
        book_shelfsResults = self.conn.fetchall()
        return book_shelfsResults
    
    def get_book_formats(self, bookId):
        formatQuery = "SELECT id, mime_type, url FROM `books_format` WHERE book_id = "+str(bookId)
        self.conn.execute(formatQuery)
        formatResults = self.conn.fetchall()
        return formatResults
    
    def get_book_info(self, bookIds, limit):
        bookQuery = "SELECT id, title, gutenberg_id FROM books_book WHERE id IN ("+str(bookIds)+") limit "+str(limit)
        self.conn.execute(bookQuery)
        bookResults = self.conn.fetchall()
        
        result = []
        
        for item in bookResults:
            item['author_info'] = BookModel().get_author_info(item['id'])
            item['language'] = BookModel().get_language_info(item['id'])
            item['subjects'] = BookModel().get_subjects_info(item['id'])
            item['book_shelves'] = BookModel().get_book_shelfs_info(item['id'])
            item['book_formats'] = BookModel().get_book_formats(item['id'])
            result.append(item)
        
        return result
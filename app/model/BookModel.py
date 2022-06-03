from ast import Str
from asyncore import file_wrapper
from ntpath import join
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
        
        # Declare string for query
        filterQuery = ""
        
        # Check values for below params
                
        # Check for book_number
        if formData['book_number'].strip():
            tempNumber = formData['book_number'].split(",")
            tempNumber = "','".join(tempNumber)
            filterQuery += "(SELECT id FROM `books_book` WHERE gutenberg_id IN ("+str("'"+tempNumber+"'")+") ) UNION "
        
        # Check for language
        if formData['language'].strip():
            tempLang = formData['language'].split(",")
            tempLang = "','".join(tempLang)
            # print("'"+tempLang+"'")
            filterQuery += "(SELECT bbl.book_id as id FROM `books_language` AS bl, `books_book_languages` AS bbl WHERE bl.id = bbl.language_id AND bl.code IN ("+str("'"+tempLang+"'")+") ) UNION "
            
        # Check for mime_type
        if formData['mime_type'].strip():
            filterQuery += "(SELECT book_id as id FROM `books_format` WHERE mime_type LIKE '%"+formData['mime_type']+"%' ) UNION "
            
        # Check for author
        if formData['author'].strip():
            filterQuery += "(SELECT bba.book_id as od FROM `books_author` as ba, `books_book_authors` as bba WHERE ba.id = bba.author_id AND ba.name LIKE '%"+str(formData['author'])+"%' ) UNION "
            
        # Check for book_title
        if formData['title'].strip():
            filterQuery += "(SELECT id FROM `books_book` WHERE title LIKE '%"+str(formData['title'])+"%' ) UNION "
            
        # Check for topic
        if formData['topic'].strip():
            filterQuery += "(SELECT bbb.book_id as id FROM `books_bookshelf` as bb, `books_book_bookshelves` as bbb WHERE bb.id = bbb.bookshelf_id AND bb.name LIKE '%"+str(formData['topic'])+"%' ) UNION "
            filterQuery += "(SELECT bbs.book_id as id FROM `books_subject` as bs, `books_book_subjects` as bbs WHERE bs.id = bbs.subject_id AND bs.name LIKE '%"+str(formData['topic'])+"%' )"
        
        # Remove extra UNION from string
        filterQuery = filterQuery.rsplit('UNION', 1)[0]
        
        # print(filterQuery)
        
        # Check for filterQuery empty string
        if filterQuery.strip():
            filterQuery += " LIMIT "+str(formData['limit'])
            
            self.conn.execute(filterQuery)
            filteredResults = self.conn.fetchall()
            
            # print(filteredResults)
            
            if filteredResults:
                # Parse book id from the result
                tempResult = ""
                for result in filteredResults:
                    tempResult += str(result['id'])+","
                filteredResults = tempResult[:-1]
                # print(filteredResults)
            else:
                filteredResults = ""
        else:
          filteredResults = ""
          
        # filteredResults = ''
        
        return self.get_book_info(filteredResults, formData['limit'])
    
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
        
        if bookIds.strip():
            whereQuery = " WHERE id IN ("+str(bookIds)+") "
        else:
            return []
        
        bookQuery = "SELECT id, title, gutenberg_id FROM books_book "+str(whereQuery)+" limit "+str(limit)
        # print(bookQuery)
        self.conn.execute(bookQuery)
        bookResults = self.conn.fetchall()
        
        result = []
        
        for item in bookResults:
            item['author_info'] = self.get_author_info(item['id'])
            item['language'] = self.get_language_info(item['id'])
            item['subjects'] = self.get_subjects_info(item['id'])
            item['book_shelves'] = self.get_book_shelfs_info(item['id'])
            item['book_formats'] = self.get_book_formats(item['id'])
            result.append(item)
        
        return result
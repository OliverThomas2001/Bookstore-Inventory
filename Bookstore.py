#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:01:38 2023

@author: oliverthomas
"""

import sqlite3
from tabulate import tabulate


#Connect to the database.
db = sqlite3.connect('bookstore_db')
cursor = db.cursor()

#Creates a list of all integers from 1 - 9999, then removes all of the integers that have already been used as IDs in the database thus leaving a list of available IDs.
available_id = [i for i in range(1, 10**4)]
cursor.execute('SELECT id FROM Library')

for identifier in cursor:
    available_id.remove(identifier[0])


#Function that takes a list of valid inputs and a prompt as arguments and ensures that the user enters a valid response from the list.
def choice_from_list(lst, input_message):
    while True:
        user_input = input(f"{input_message}")
        if user_input in lst:
            break
        else:
            print("The value you have entered is invalid. ")
    return user_input


#Function that takes a 2D list as an argument and displays the information in the form of a table.
def view_all(book_data):
    cursor.execute('SELECT id FROM Library')
    lst = cursor.fetchall()
    if len(lst) == 0:
        print("""
The database has no entries at this time.
""")
    
    else:
        print()
        print(tabulate(book_data, headers = ['ID', 'Title', 'Author', 'Quantity'], tablefmt = 'presto'))
        print()


#Function that adds data about books to the database.
def add_book():
    
    title1 = input("Please enter the title of the book you wish to add to the database: ")
    
    author1 = input("Please enter the name of the author of the book: ")
    
    #Counts the number of data entries that match the given conditions.
    cursor.execute(f'SELECT COUNT(id) FROM Library WHERE Title = "{title1}" AND Author = "{author1}"')
    
    sol = cursor.fetchone()
    
    #If this book already exists in the database then an error message will be displayed.
    if sol[0]>0:
        print("""
The book you have entered already exists in the database. Please use the edit feature to update the entry.
              """)
        return
    
    #Asks the user to input a non-negative integer as the quantity if books in stock.
    while True:
        try:
            quantity = int(input("Please enter the number of copies of this book in stock: "))
            if quantity>=0:
                break
            else:
                print("Please enter an integer greater than or equal to zero.")
        
        except ValueError:
            print("""You have entered a non-number character.
                  Please enter an integer greater than or equal to zero.""")
        
    #Updates the database with the new entry using the smallest available ID.
    cursor.execute(f'INSERT into Library(id, Title, Author, Quantity) VALUES ({min(available_id)}, "{title1}", "{author1}", "{quantity}")')
    db.commit()
    
    available_id.remove(min(available_id))


#Function that searches through the database for a book/collection of books given the search type as an argument (i.e. search by author, title or ID).
def search(search_type):
    
    query = input(f'Please enter the {search_type} of the book(s) you are looking for: ')
    
    cursor.execute(f'SELECT * FROM Library WHERE {search_type} = "{query}"')
    
    search_data = cursor.fetchall()
    view_all(search_data)


#Function that allows the user to update data in the database or delete an entrant.
def update_entry():
    
    #Gives a list of all valid Ids
    cursor.execute('SELECT id FROM Library')
    lst = cursor.fetchall()
    id_list = [str(lst[i][0]) for i in range(len(lst))]
    
    #Returns nothing if there are no entries to update.
    if len(id_list)==0:
        print("The database currently has no entries to update.")
        return
    
    cursor.execute('SELECT * FROM Library')
    book_data = cursor.fetchall()
    view_all(book_data)
    
    update_ID = choice_from_list(id_list, 'Please choose the ID value of the entry you would like to update: ')
    
    update_type = choice_from_list([str(i) for i in range(1,6)], '''1 - Update Book Title
2 - Update Author
3 - Update Quantity
4 - Delete Entry
5 - Exit

Please select the entry you would like to update from the above menu.
''')
    
    update_dict = {'1':'Title', '2':'Author', '3':'Quantity'}

    if update_type == '5':
        pass
    
    elif update_type == '4':
        cursor.execute(f'DELETE FROM Library WHERE id = "{update_ID}"')
        db.commit()
        
        update_dict = {'1':'Title', '2':'Author', '3':'Quantity', '4':' ' , '5':' '}
    
    elif update_type == '3':
        while True:
            try:
                quantity = int(input("Please enter the number of copies of this book in stock: "))
                if quantity>=0:
                    break
                else:
                    print("Please enter an integer greater than or equal to zero.")
            
            except ValueError:
                print("""You have entered a non-number character.
                      Please enter an integer greater than or equal to zero.""")
    
        cursor.execute(f'UPDATE Library SET {update_dict[update_type]} = {quantity} WHERE id = "{update_ID}"')
        db.commit()
        
    else:
        new_entry = input(f"Please enter the new {update_dict[update_type]}: ")
        
        cursor.execute(f'UPDATE Library SET {update_dict[update_type]} = "{new_entry}" WHERE id = "{update_ID}"')
        db.commit()
    
    
while True:
#===============MENU=================
    print("""1 - View all books
2 - Search for a book / collection of books
3 - Add a new book to the database
4 - Update an entry
5 - Exit
    """)
    
    menu_choice = choice_from_list([str(i) for i in range(1, 6)], "Please select the function you would like to perform from the above list. ")
    
#===============VIEW ALL BOOKS=================
    
    if menu_choice == '1':
        cursor.execute('SELECT * FROM Library')
        book_data = cursor.fetchall()
        view_all(book_data)
        
        
#===============SEARCH=================
    
    if menu_choice =='2':
        
        cursor.execute('SELECT id FROM Library')
        lst = cursor.fetchall()
        if len(lst) == 0:
            print("""
The database has no entries at this time.
""")
        
        else:
        
            print("""1 - Search by Title
2 - Search by Author
3 - Search by ID
4 - Exit
        """)
        
            search_choice = choice_from_list([str(i) for i in range(1,5)], "Please select the search type you would like to perform from the above list. ")
            
            search_dict = {'1':'Title', '2':'Author', '3':'id'}
            
            if search_choice == '4':
                pass
            else:
                search(search_dict[search_choice])
            

#===============ADD NEW BOOK=================

    if menu_choice == '3':
        
        add_book()
        print('Your entry has been added to the database.')
        
        
#===============UPDATE ENTRY=================
    
    if menu_choice == '4':
        update_entry()
        
        
#===============EXIT========================
    if menu_choice == '5':
        break



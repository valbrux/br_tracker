import sqlite3
import argparse
import os.path
import datetime

db_file = ".br-tracker.db"


def initDb(c):
    c.execute('''CREATE TABLE IF NOT EXISTS books(date_start text,book_name text,pages integer,current_page integer)''')

def addBook(book_name,pages,c):
    book = (datetime.date.today(),book_name,pages,0)
    c.execute('''INSERT INTO books VALUES(?,?,?,?)''',book)

def deleteBook(book_name,c):
    c.execute('''DELETE FROM books WHERE book_name=?''',(book_name,))

def updateBook(book_name,current_page,c):
    c.execute('''UPDATE books SET current_page=? WHERE book_name=?''',(current_page,book_name))
        
def printProgressBar(total,current,prefix = '',suffix = '',decimals = 1,length = 50, fill = 'x'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (current/float(total)))
    filledLength = int(length*current//total)
    bar = fill * filledLength + '-' * (length-filledLength)
    print('  |%s| %s%% %s %s/%s pages\r' % (bar,percent,suffix,current,total), end='')

def showBooks(c):
   for row in c.execute('''SELECT * FROM books ORDER BY book_name ASC'''):
       print("\033[1m%s\033[0m" % row[1])
       print("  Start date:%s " % row[0])
       printProgressBar(row[2],row[3])
       print("")
       print("")

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    initDb(c)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add',nargs=2,metavar=('book','pages'),help="Add a new book")
    group.add_argument('--dele',nargs=1,metavar=('book'),help="Delete an existing book")
    group.add_argument('--upd',nargs=2,metavar=('book','current'),help="Update pages")
    group.add_argument('--show',action='store_true',help="Progress show")
    results = parser.parse_args()
    if results.add is not None: 
        addBook(results.add[0],results.add[1],c)
    elif results.dele is not None:
        deleteBook(results.dele[0],c)
    elif results.upd is not None:
        updateBook(results.upd[0],results.upd[1],c)
    elif results.show is not None:
        showBooks(c)
    try:
        conn.commit()
    except sqlite3.Error as er:
        print('error',er.message)
    conn.close()

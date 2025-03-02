import settings
import sqlite3
from pprint import pprint
import datetime 

conn = None
curs = None

def do(query, params = []):
    curs.execute(query, params)
    conn.commit()


def close():
    curs.close()
    conn.close()


def open():
    global conn, curs
    conn = sqlite3.connect(settings.DB_URL)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

def outer(func):
    def inner(*args, **kwargs):
        open()
        res = func(*args, **kwargs)
        close()
        return res

    return inner

@outer
def getUser(login):
    query = "SELECT * FROM user WHERE login=?"
    do(query,params=[login])
    user = curs.fetchone()
    return user

@outer
def updateUser(data):
    query = '''
        UPDATE user
        SET 
            login = ?,
            password = ?,
            name = ?,
            image = ?,
            description = ?
        WHERE login=?;
    '''
    do(
       query,
       [
           data.get("login"),
           data.get("password"),
           data.get("name"),
           data.get("image"),
           data.get("description"),
           data.get("login"),
       ]
    )

def getPostsByCategory(category_id):
    open()
    query = "SELECT * FROM post WHERE category_id=?"
    
    do(query, params=[category_id])
    all_post = curs.fetchall()
    
    close()
    return all_post

def getIdByCategory(category_name):
    open()
    query = "SELECT id FROM category WHERE name=?"
    
    do(query, params=[category_name])
    all_id = curs.fetchone()['id']
    
    close()
    return all_id

def addPost(category_id, post, title, filename):
    open()
    query = ''' 
            INSERT INTO post(category_id, text, image, datetime, title )
            VALUES(?,?,?,?,?)
            '''
    
    carent_date = datetime.datetime.now()

    do(query,params=[category_id, post, filename, carent_date, title])
    close()
    
def delPost(post_id):
    open()
    query = "DELETE FROM post WHERE id=?"
    
    do(query,params=[post_id])
    close()



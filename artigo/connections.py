from django.conf import settings

AUTH_TOKEN = settings.FIREBASE_AUTH_TOKEN
db = settings.FIREBASE.database()

"""
Insert record into Firebase database 
@params - table - Table name in which record is to inserted
        - key   - Record identifier
        - data  - Record to be inserted
"""
def insert(table, key, data):
    db.child(table).child(key).set(data, AUTH_TOKEN)

"""
Insert record into Firebase database without specifying key
@params - table - Table name in which record is to inserted
        - data  - Record to be inserted
"""
def push(table, data):
    db.child(table).push(data, AUTH_TOKEN)

"""
Get all records from Firebase database
@params - table - Table name in which record is to inserted
"""
def fetch(table):
    return db.child(table).get(AUTH_TOKEN).val()

"""
Get one record from Firebase database 
@params - table - Table name in which record is to inserted
        - key   - Key for which record needs to be searched 
"""
def fetch_one(table, key):
    return db.child(table).child(key).get(AUTH_TOKEN).val()

"""
Delete record from Firebase database
@params - table - Table name from which record is to be deleted
        - key   - Record identifier
"""
def delete(table, key):
    return db.child(table).child(key).remove(AUTH_TOKEN)

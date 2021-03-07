#!/usr/bin/python3

import cgi,cgitb
import mysql.connector

form = cgi.FieldStorage()
messageKey = form.getvalue('message-key')

db = mysql.connector.connect(host='localhost', user='ryanh', passwd='k33p1ts1mpl3', db='anonymsg', auth_plugin='mysql_native_password')
cursor = db.cursor()

def checkExistence(msgKey,cursor,db):
    sql = 'SELECT EXISTS(SELECT * FROM messages WHERE BINARY message_key = "{}");'.format(msgKey)
    cursor.execute(sql)
    msgExistence = cursor.fetchone()
    return msgExistence[0]

def checkType(msgKey,cursor,db):
    sql = 'SELECT message_type FROM messages WHERE BINARY message_key = "{}";'.format(msgKey)
    cursor.execute(sql)
    msgType = cursor.fetchone()
    return msgType[0]

def eraseMessage(msgKey,cursor,db):
    sql = 'DELETE FROM messages WHERE BINARY message_key = "{}";'.format(msgKey)
    cursor.execute(sql)

def retrieveMessage(msgKey,cursor,db):
    sql = 'SELECT message_content FROM messages WHERE BINARY message_key = "%s";' % (msgKey)
    cursor.execute(sql)
    msgContent = cursor.fetchone()
    return msgContent[0]

print('Content-Type: text/html')
print()
print('<!DOCTYPE html>')
print('<html lang="en">')
print('<head>')
print('<meta charset="utf-8">')
print('<meta name="viewport" content="width=device-width,initial-scale=1">')
print('<link rel="stylesheet" type="text/css" href="/css/styles.css">')
print('</head>')
print('<body>')

checkExistence = checkExistence(messageKey,cursor,db)
if checkExistence:
    checkType = checkType(messageKey,cursor,db)
    if checkType:
        print('<p>This message is private!</p>')
        print('<p>{}</p>'.format(retrieveMessage(messageKey, cursor, db)))
        eraseMessage(messageKey,cursor,db)
    else:
        print('<p>This message is public!</p>')
        print('<p>{}</p>'.format(retrieveMessage(messageKey, cursor, db)))
else:
    print('<p>There is no message stored using this key!</p>')

print('</body>')
print('</html>')

db.commit()
cursor.close()
db.close()

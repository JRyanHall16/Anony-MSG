#!/usr/bin/python3

import cgi,cgitb
import mysql.connector

# open and store information from form.
form = cgi.FieldStorage()
messageContent = form.getvalue('message-content')
messageKey = form.getvalue('message-key')
messageType = 0 if form.getvalue('message-type') else 1

# connect to database.
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

def insertMessage(msgKey,msgContent,msgType,cursor,db):
    sql = 'INSERT INTO messages (message_content, message_key, message_type) VALUES ("{}", "{}", {});'.format(msgContent,msgKey,msgType)
    cursor.execute(sql)

#   if exists[0]:
#        print('<p>A message already exists!</p>')
        # check to see if it is a one-time access message.
#        sql = 'SELECT message_type FROM messages WHERE message_key = "%s";' % (messageKey)
#        cursor.execute(sql)
#        isPrivate = cursor.fetchone()
#        if isPrivate[0]:
#            print('<p>This message is private!</p>')
#        else:
#            print('<p>This message is public!</p>')
#            sql = 'SELECT message_content FROM messages WHERE message_key = "%s";' % (messageKey)
#            cursor.execute(sql)
#            message = cursor.fetchone()
#            print(message[0])
#    else:
#        insertMessage(messageKey, messageContent, messageType, cursor, db)
#        print('<p>Your message was stored!</p>')

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
        eraseMessage(messageKey,cursor,db)
        insertMessage(messageKey,messageContent,messageType,cursor,db)
        print('<p>A message was replaced.</p>')
    else:
        print('There is already a message stored with this key!</p>')
else:
    insertMessage(messageKey,messageContent,messageType,cursor,db)
    print('<p>Your message was stored!</p>')

print('<p>Message: %s</p>' % messageContent)
print('<p>Message Key: %s</p>' % messageKey)
if form.getvalue('message-type'):
    print('yes!')
else:
    print('no!')

print('<p>Message Type: %s</p>' % messageType)

print('</body>')
print('</html>')

db.commit()
cursor.close()
db.close()

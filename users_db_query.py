host = "127.0.0.1"
user = "postgres"
password = "0000"
dbname = "vacation"
port = 5432

import psycopg2
from psycopg2 import sql
import re

#name - название локации, time - минимальное время для прогулки в этой локации, style - тип локации, persons - максимальное количество людей в группе для локации

def __connect():
    """Инициализация соединения с бд"""
    conn=psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )
    return conn
def userNoExist(id:int):
    conn=__connect()
    cursor=conn.cursor()
    cursor.execute('SELECT uid FROM users WHERE uid=%s;', (id,))
    result=str(cursor.fetchone())
    conn.close()
    #print(result)
    if re.search(r'\bNone\b', result):
    #if result == "None": 
        return True
    else:
        return False
def addUser(id:int):
    """добавления пользователя из телеграма в БД"""
    try:
        conn=__connect()
        cursor=conn.cursor()
        cursor.execute('INSERT INTO users VALUES (%s, %s, %s);', (id,3,'{1,2,3}',))
        #print(id)
        conn.commit()
        conn.close()
    except:
        print('error with user add')
def changeHistory(id:int,history:int):
    """изменение истории выбора мест"""
    try:
        #print(history)
        #print(id)
        conn=__connect()
        cursor=conn.cursor()
        if userNoExist(id): addUser(id) #if user doesn't exist, create user
        cursor.execute('SELECT history FROM users WHERE uid=%s;', (id,))
        #result=int(cursor.fetchone()[0])
        result=cursor.fetchone()[0]
        new_history='{'+str(result[1])+','+str(result[2])+','+str(history)+'}'
        
        cursor.execute('UPDATE users SET history = %s WHERE uid=%s;',(new_history,id,))
        conn.commit()
        conn.close()
    except:
        print('error with change model')

def selectHistory(id:int):
    """вывод истории у пользователя"""
    try:
        conn=__connect()
        cursor=conn.cursor()
        if userNoExist(id): addUser(id) #if user doesn't exist, create user
        cursor.execute('SELECT history FROM users WHERE uid=%s;', (id,))
        result=cursor.fetchone()[0]
        #print(result) #print int token
        conn.close()
        return result
    except:
        return {1,2,3}

def token(id:int):
    """вывод количества токенов у пользователя"""
    try:
        conn=__connect()
        cursor=conn.cursor()
        if userNoExist(id): addUser(id) #if user doesn't exist, create user
        cursor.execute('SELECT token FROM users WHERE uid=%s;', (id,))
        result=int(cursor.fetchone()[0])
        #print(result) #print int token
        conn.close()
        return result
    except:
        return 0

def reduceTokens(id:int):
    """уменьшение количества токенов на 1"""
    try:
        conn=__connect()
        cursor=conn.cursor()
        if userNoExist(id): addUser(id) #if user doesn't exist, create user
        cursor.execute('SELECT token FROM users WHERE uid=%s;', (id,))
        tokens=int(cursor.fetchone()[0])-1
        print(tokens)
        cursor.execute('UPDATE users SET token=%s WHERE uid=%s;',(tokens,id,))
        conn.commit()
        conn.close()
    except:
        print('error with reduce tokens')


##___examples:____

#changeHistory(666000666,4)
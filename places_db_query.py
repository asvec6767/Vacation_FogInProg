host = ""
user = ""
password = ""
dbname = ""
port = 0

import psycopg2
from psycopg2 import sql
import re
import geocoder

#name - название локации, time - минимальное время для прогулки в этой локации, style - тип локации, persons - максимальное количество людей в группе для локации

def __connect(name:str):
    """Инициализация соединения с бд"""
    password=''
    if name=="postgres": password="0000" 
    #print('name: '+str(name)+'pass: '+str(password))
    connection = psycopg2.connect(
        host=host,
        user=name,
        password=password,
        database=dbname
    )
    return connection

def selectPlaces(time:int,style:str,persons:int):
    """Вывод мест отдыха согласно выбранным требованиям"""
    conn=__connect("postgres")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM places WHERE time=%s AND style=%s AND persons>=%s;",(time,style,persons,))
    result=cursor.fetchall()
    conn.close()
    return result

def selectPlacesByID(id:int):
    """Вывод мест отдыха по id"""
    conn=__connect("postgres")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM places WHERE id=%s;",(id,))
    result=cursor.fetchall()
    conn.close()
    return result

def selectPlace_data(id:int):
    """вывлд параметров места по id"""
    conn=__connect("postgres")
    cursor=conn.cursor()
    cursor.execute("SELECT time,style,persons FROM places WHERE id=%s;",(id,))
    result=cursor.fetchall()
    conn.close()
    return result[0]

def addSuggest(name:str):
    """Добавление пользовательского места отдыха в базу данных в таблицу предложений"""
    try:
        conn=__connect("postgres")
        cursor=conn.cursor()
        cursor.execute("INSERT INTO suggest(name) VALUES (%s);",(name,))
        conn.commit()
        conn.close()
        return True 
    except:
        print("add query exception with "+name)
        return False



##___examples:____
#addPlace('Платоновский парк',1,'парк',10)
#print(selectPlaces(10,'парк',2))

def place_dbToString(tuple):
    time=['1-2ч', '3-5ч', '6ч и более','2 дня']
    person=['один','пара','с детьми','компания']
    result="📍Место: "+tuple[1]+"\n⏰️Время: "+time[int(tuple[2])-1]+"\n🏃‍♂️Тип отдыха: "+tuple[3]
    result += '\n🌐Адрес: '+geocoder.get_adress(float(str(tuple[5]).split()[0]),float(str(tuple[5]).split()[1]))
    return result

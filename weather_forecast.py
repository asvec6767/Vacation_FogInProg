import requests
import json

    
def get_weather():
    #city=message.text.strip().lower()
    city='Tula'
    res=requests.get('https://api.openweathermap.org/data/2.5/weather?q=Tula&appid=TOKEN&units=metric&lang=ru')
    data=json.loads(res.text)
    temp=data["main"]["temp"]
    clouds=data["weather"][0]["description"]
    #if ("descrption"="overcast clouds") 
    result=('Погода в Туле: '+'\n'+f'🌡температура +{temp}'+'\n'+f'🌤{clouds}')
    return result
   
   


import requests
import json
#API='4095a2240094bfb5980d8e80c064d0af'

    
def get_weather():
    #city=message.text.strip().lower()
    city='Tula'
    res=requests.get('https://api.openweathermap.org/data/2.5/weather?q=Tula&appid=token&units=metric&lang=ru')
    data=json.loads(res.text)
    temp=data["main"]["temp"]
    clouds=data["weather"][0]["description"]
    #if ("descrption"="overcast clouds") 
    result=('Погода в Туле: '+'\n'+f'🌡температура +{temp}'+'\n'+f'🌤{clouds}')
    return result
   
   


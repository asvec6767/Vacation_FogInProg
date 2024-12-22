from math import cos, asin, sqrt, pi
from random import randrange
import places_db_query as places
import gpt
import geocoder

#использование формулы Хаверсина для вычисления расстояния
def _distance(lat1, lon1, lat2, lon2):
    r = 6371 # km
    p = pi / 180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    dist= 2 * r * asin(sqrt(a))
    return dist

def create_distance(time_str:str):
    """Главный метод построения маршрута"""
    try:
        #print(time_str)
        time=int(time_str)
        #print(time)
        if time<0:
            result='Время некорректно (меньше 0), введите запрос заново'
        elif time<5:
            result='Время слишком мало (меньше 5), попробуйте найти места'
        elif time<10:
            result=_create_detail_distance(1,3)
        elif time<20:
            result=_create_detail_distance(1,3)
        elif time<40:
            result=_create_detail_distance(2,5)
        else:
            result=_create_detail_distance(2,7)
        return result
    except:
        result='Извините, маршрут не был построен!'
        return result

        
def _dist_to_string(place, dist):
    places_name=[]
    for i in range(0,len(place),+1):
        places_name.append(place[i][1])
    
    dist_name=gpt.prompt_distance_name(places_name)

    result=f'Маршрут "{dist_name}": \n\n'
    count=len(place)


    for i in range(0,count,+1):
        result+=places.place_dbToString(place[i])
        #result+='\n🌐Адрес: '+geocoder.get_adress(float(str(place[i][5]).split()[0]),float(str(place[i][5]).split()[1]))
        if i+1<count:
            result+=f'\n\nВремя на дорогу между пунктами {i+1} и {i+2}: '
            if dist[i]<=2:
                result+=str(int(dist[i]/5*60))
                result+=' мин. пешком\n\n'
            else:
                result+=str(int(dist[i]/20*60))
                result+=' мин. на транспорте\n\n'
              
    return result

def _create_detail_distance(time:int,count:int):
    style=['музей','ресторан', 'парк']
    place=[]
    dist=[]
    for i in range(0,count,+1):
        #print('i='+str(i))
        #print(style[i%3]+'\n')
        #print(str(time)+'\n')
        if style[i%3]=='ресторан':
            place_arr=places.selectPlaces(1,str(style[i%3]),1)#массив мест из базы данных
        else:
            place_arr=places.selectPlaces(int(time),str(style[i%3]),1)#массив мест из базы данных

        place.append( place_arr[randrange(len(place_arr))] )#конкретное место в виде массива данных о нем
        if i>=1:
            #print('location : '+str(place[i][5]))
            loc2=str(place[i][5]).split()#преобразование строки в координаты
            latitude2=float(loc2[0])
            longitude2=float(loc2[1])

            loc1=str(place[i-1][5]).split()#преобразование строки в координаты
            latitude1=float(loc1[0])
            longitude1=float(loc1[1])

            dist.append(_distance(latitude1,longitude1,latitude2,longitude2))
    
    result=_dist_to_string(place,dist)

    return result

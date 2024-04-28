import requests
import json

def get_adress(latitude:float, longitude:float):
    """Получение адреса по GPS координатам"""
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&lang=ru&format=json&apiKey=token"
    response = requests.get(url)
    adress=json.loads(response.text)
    adress_result=adress["results"][0]["formatted"]
    result=(f'{adress_result}')
    return result
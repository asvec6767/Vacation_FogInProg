import telebot
from telebot import types

import random
from random import randrange
import os
import re

import places_db_query as places, users_db_query as users #файлы для базы данных
import gpt #файл с чатои гпт
import weather_forecast #погода по апи
import distant #расчет расстояния
import predict_new as predict #предсказания

bot=telebot.TeleBot('telegram_token')

def create_markup():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
  btn = types.KeyboardButton("Построить маршрут")
  markup.add(btn)
  btn = types.KeyboardButton("Найти место")
  markup.add(btn)
  btn = types.KeyboardButton("Добавить место")
  markup.add(btn)
  btn = types.KeyboardButton("Посмотреть погоду")
  markup.add(btn)
  btn = types.KeyboardButton("Новогодний квест")
  markup.add(btn)
  return markup

#обработка старт
@bot.message_handler(commands=['start'])
def main (message):
  try:
    if(users.userNoExist(message.from_user.id)):
      users.addUser(message.from_user.id)

    bot.send_message(message.chat.id,f'Привет, {message.from_user.first_name}! Я - тг-бот, позволяющий тебе подобрать увлекательный маршрут по Туле и Тульской области.')
     #получаем id и имени пользователя для записи в бд
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    print(f'Новый пользователь {us_name}')
    
   # db_table_val(id=us_id, name=us_name)
   # conn.close()
    markup = create_markup()
    bot.send_message(message.chat.id, text="Нажимай кнопку снизу и скорее отправляйся в путешествие!", reply_markup=markup)
    bot.register_next_step_handler(message, on_click_find_time)
  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())

#действие по кнопке "найти маршрут"  
@bot.message_handler(content_types=['text'])
def on_click_find_time(message):
  try:
    print(f'Пользователь: {message.from_user.first_name}, действие: {message.text}')
    if message.text=="Построить маршрут":
      bot.send_message(message.chat.id, 'Отправь время в часах для маршрута:', reply_markup=types.ReplyKeyboardRemove())
      bot.register_next_step_handler(message, on_click_time_to_travel)
    elif message.text=="Найти место":
      keyboard = types.InlineKeyboardMarkup()
      one_k = types.InlineKeyboardButton(text='1-2ч', callback_data='1')
      two_k = types.InlineKeyboardButton(text='3-5ч', callback_data='2')
      three_k = types.InlineKeyboardButton(text='6ч и более', callback_data='3')
      four_k = types.InlineKeyboardButton(text='2 дня', callback_data='4')
      keyboard.add(one_k,two_k, three_k)
      keyboard.add( four_k)
      bot.send_message(message.chat.id, 'Выбери сколько времени тебе потребуется для изучения достопримечательностей:', reply_markup=keyboard)
      bot.register_next_step_handler(message, on_click_find_persons)
    elif message.text=="Посмотреть погоду":
      result=weather_forecast.get_weather()
      markup=create_markup()
      bot.send_message(message.chat.id, text=result, reply_markup=markup)
    elif message.text=="Добавить место":
      bot.send_message(message.chat.id, 'Отправь название места, можешь добавить краткую информацию о нем:', reply_markup=types.ReplyKeyboardRemove())
      bot.register_next_step_handler(message, on_click_add_suggest)
    elif message.text=="Новогодний квест":
      bot.send_message(message.chat.id, 'Напиши стишок Деду Морозу, чтобы получить новогодний вайб: (Пример - Новый год стучится в дом! Много снега за окном!)', reply_markup=types.ReplyKeyboardRemove())
      bot.register_next_step_handler(message, on_click_new_year_quest)
    else:#обработка исключений, непредвиденное сообщение
      bot.send_message(message.chat.id,'<b>Я вас не понял</b>', parse_mode='html') 
  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())
     
def on_click_time_to_travel(message):#подбор места
  try:
    bot.send_message(message.chat.id, '🧭Подбираем место, пожалуйста подождите...')
    result=distant.create_distance(message.text)
    markup = create_markup()

    bot.send_message(message.chat.id, text=result, reply_markup=markup)
  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())

def on_click_add_suggest(message):
  try:
    text=''
    if(users.userNoExist(message.from_user.id)):
      users.addUser(message.from_user.id)
    elif(int(users.token(message.from_user.id))>0):
      users.reduceTokens(message.from_user.id)
      places.addSuggest(str(message.text))
      text='Спасибо за предложение, мы обязательно рассмотрим его добавление в маршруты!'
    else:
      text='Превышено количество количество предложений объектов'
    markup = create_markup()
    
    bot.send_message(message.chat.id, text=text, reply_markup=markup)
  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())

def on_click_new_year_quest(message):
  """Функция обработки новогоднего стишка"""
  try:
    bot.send_message(message.chat.id, '🧭Обрабатываем запрос, пожалуйста подождите...')
    text = re.sub(r'\d+', '', str(message.text))
    text = text[0:100]
    print (f'Пользователь: {message.from_user.first_name} Написал новогодний стих: {text}')
    if gpt.prompt_check_poem(text):#если пользователь написал стишок
      print (f'Пользователь: {message.from_user.first_name} получил ответ ДА на свой стих')
      newYearList = [18,30,37,38,39]#список новогодних мест
      arrPlaces = places.selectPlacesByID(random.choice(newYearList))#получения случайного места из списка
      
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(2,'парк',1)#array of places
      result_tuple=arrPlaces[randrange(len(arrPlaces))]
      result=places.place_dbToString(result_tuple)
      result+="\n📃Описание: "+gpt.prompt(result_tuple[1])#генерация описания в чат гпт
    
      loc=str(result_tuple[5]).split()#преобразование строки в координаты
      latitude=float(loc[0])
      longitude=float(loc[1])

      img_path = os.path.join(os.path.dirname(__file__),f'img\\{result_tuple[0]}.jpg')
      if os.path.exists(img_path):
        bot.send_photo(message.chat.id, open(img_path, 'rb'), caption=result_tuple[1])#отправка картинки пользователю при ее наличии

      keyboard = types.InlineKeyboardMarkup()
      one_k = types.InlineKeyboardButton(text='Добавить в избранное', callback_data='f'+str(result_tuple[0]))#добавить в историю id
      keyboard.add(one_k)
      one_k = types.InlineKeyboardButton(text='Просмотреть предложения (в разработке)', callback_data='p'+str(result_tuple[0]))#сгенерировать место
      keyboard.add(one_k)
      bot.send_message(message.chat.id, str(result),reply_markup=keyboard)#отправка описания

      markup = create_markup()
      bot.send_location(message.chat.id, latitude=latitude,longitude=longitude,reply_markup=markup)#отправка точки на карте
    else:
      answer = "Хо-хо-хо, кто-то плохо вел себя в этом году! Попробуй еще раз рассказать мне стишок..."
      bot.send_message(message.chat.id, str(answer), reply_markup=create_markup())
  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())
    
def on_click_add_predict(message):
  """работа с предсказаниями"""
  try:
    text=''
    #print(message)
    #print(message.chat.id)
    if(users.userNoExist(message.chat.id)):
      users.addUser(message.chat.id)
      text='Недостаточно объектов в избранном'
      bot.send_message(message.chat.id, text=text, reply_markup=create_markup())
    else:
      bot.send_message(message.chat.id, '🧭Подбираем место, пожалуйста подождите...')
      history=(users.selectHistory(message.chat.id))
      #print(history)
      result=predict.predict(history)
      
      time=result[0]
      style=result[1]
      persons=result[2]

      arrPlaces=places.selectPlaces(time,style,persons)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(time,style,0)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(1,style,persons)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(1,style,0)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(2,'парк',1)#array of places
      result_tuple=arrPlaces[randrange(len(arrPlaces))]
      result=places.place_dbToString(result_tuple)
      result+="\n📃Описание: "+gpt.prompt(result_tuple[1])#генерация описания в чат гпт

      loc=str(result_tuple[5]).split()#преобразование строки в координаты
      latitude=float(loc[0])
      longitude=float(loc[1])

      img_path = os.path.join(os.path.dirname(__file__),f'img\\{result_tuple[0]}.jpg')
      if os.path.exists(img_path):
        bot.send_photo(message.chat.id, open(img_path, 'rb'), caption=result_tuple[1])#отправка картинки пользователю при ее наличии

      keyboard = types.InlineKeyboardMarkup()
      one_k = types.InlineKeyboardButton(text='Добавить в избранное', callback_data='f'+str(result_tuple[0]))#добавить в историю id
      keyboard.add(one_k)
      bot.send_message(message.chat.id, str(result),reply_markup=keyboard)#отправка описания

      markup = create_markup()
      bot.send_location(message.chat.id, latitude=latitude,longitude=longitude,reply_markup=markup)#отправка точки на карте

  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())



@bot.callback_query_handler(func=lambda call: True)
def on_click_find_persons(call):
  try:
    if call.data[0]=='p':
      on_click_add_predict(call.message)
      print(f'Пользователь {call.from_user.first_name} - запрос предсказания')

    elif call.data[0]=='f':
      if(users.userNoExist(call.from_user.id)):
        #print(call)
        #print(call.from_user.id)
        users.addUser(call.from_user.id)
      else:
        history=int(call.data.replace('f','',1))
        users.changeHistory(call.from_user.id, history)
        #print(history)
      murkup=create_markup()
      bot.send_message(call.message.chat.id, 'Выбранное место добавлено в избранное', reply_markup=murkup)
      print(f'Пользователь {call.from_user.first_name} - добавление в избранное')
    elif len(call.data)==1:
      keyboard = types.InlineKeyboardMarkup()
      one_k = types.InlineKeyboardButton(text='один', callback_data=str(call.data)+'1')
      two_k = types.InlineKeyboardButton(text='пара', callback_data=str(call.data)+'2')
      three_k = types.InlineKeyboardButton(text='с детьми', callback_data=str(call.data)+'3')
      four_k = types.InlineKeyboardButton(text='компания', callback_data=str(call.data)+'4')

      keyboard.add(one_k, two_k)
      keyboard.add(three_k, four_k)
      bot.send_message(call.message.chat.id, 'Выбери свою компанию:', reply_markup=keyboard)
    
    elif len(call.data)==2:
      keyboard = types.InlineKeyboardMarkup()
      one_k = types.InlineKeyboardButton(text='парк', callback_data=str(call.data)+'1')#парк
      two_k = types.InlineKeyboardButton(text='музей', callback_data=str(call.data)+'2')#музей
      three_k = types.InlineKeyboardButton(text='активный отдых', callback_data=str(call.data)+'3')#актив
      four_k = types.InlineKeyboardButton(text='ресторан', callback_data=str(call.data)+'4')#ресторан

      keyboard.add(one_k, two_k)
      keyboard.add(three_k, four_k)
      bot.send_message(call.message.chat.id, 'Выбери предпочитаемый тип отдыха:', reply_markup=keyboard)\

    else:
      bot.send_message(call.message.chat.id, '🧭Подбираем место, пожалуйста подождите...')
      #print(call.data)
      
      time=str(call.data[0])
      persons=str(call.data[1])
      arrStyle=['парк', 'музей', 'актив', 'ресторан']
      #print(arrStyle[1])
      style=arrStyle[int(call.data[2])-1]

      #print('[ ' +time+' '+ style+' '+persons+' ]')
      arrPlaces=places.selectPlaces(time,style,persons)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(time,style,0)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(1,style,persons)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(1,style,0)#array of places
      if len(arrPlaces)==0: arrPlaces=places.selectPlaces(2,'парк',1)#array of places
      result_tuple=arrPlaces[randrange(len(arrPlaces))]
      result=places.place_dbToString(result_tuple)
      result+="\n📃Описание: "+gpt.prompt(result_tuple[1])#генерация описания в чат гпт

      loc=str(result_tuple[5]).split()#преобразование строки в координаты
      latitude=float(loc[0])
      longitude=float(loc[1])

      img_path = os.path.join(os.path.dirname(__file__),f'img\\{result_tuple[0]}.jpg')
      if os.path.exists(img_path):
        bot.send_photo(call.message.chat.id, open(img_path, 'rb'), caption=result_tuple[1])#отправка картинки пользователю при ее наличии

      keyboard = types.InlineKeyboardMarkup()
      one_k = types.InlineKeyboardButton(text='Добавить в избранное', callback_data='f'+str(result_tuple[0]))#добавить в историю id
      keyboard.add(one_k)
      one_k = types.InlineKeyboardButton(text='Просмотреть предложения (в разработке)', callback_data='p'+str(result_tuple[0]))#добавить в историю id
      keyboard.add(one_k)
      bot.send_message(call.message.chat.id, str(result),reply_markup=keyboard)#отправка описания

      markup = create_markup()
      bot.send_location(call.message.chat.id, latitude=latitude,longitude=longitude,reply_markup=markup)#отправка точки на карте

  except:
    try:
      on_click_find_time(call.message)
    except:
      on_click_find_time(call)

@bot.message_handler(content_types=['location'])
def handle_loc(message):
  try:
    bot.send_message(message.chat.id, text="Ура, вы нашли пасхалку! А еще мы знаем ваше местоположение, ха-ха-ха", reply_markup=create_markup())
    print(f'Пользователь {message.from_user.first_name} нашел пасхалку')
  except:
    bot.send_message(message.chat.id, text="Упс... что-то пошло не так, попробуйте позже", reply_markup=types.ReplyKeyboardRemove())
    
bot.polling(non_stop=True)

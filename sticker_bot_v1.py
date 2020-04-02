import telebot;
import pandas as pd 
import numpy as np

# Указываем токен
bot= telebot.TeleBot('1060588156:AAFdHkmHHoiLge3ZGEABmhRAb2SO6_sLGa8');
import random
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
#Глобальный список
Save_user=[]
  
class UserMale():
    def _init_(self,sex='no male'):
        self.count_for_male=0
        self.sex="no male"
        
    def male_female(sex): 
        return sex
        
        # Метод, который получает сообщения и обрабатывает их
    @bot.message_handler(content_types=['audio', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
    def get_text_messages(message):
        if message.text == "Привет" or message.text == "привет":
            bot.send_message(message.from_user.id, "Привет, хочешь найти себе пару с помощью стикеров")        
                # Готовим кнопки
            keyboard = types.InlineKeyboardMarkup()
                # По очереди готовим текст и обработчик для каждого знака зодиака
            key_male = types.InlineKeyboardButton(text='Парень', callback_data='Парень')
                # И добавляем кнопку на экран
            keyboard.add(key_male)
            key_female = types.InlineKeyboardButton(text='Девушка', callback_data='Девушка')
            keyboard.add(key_female)
                # Показываем все кнопки сразу и пишем сообщение о выборе
            bot.send_message(message.from_user.id, text='Кто вы?', reply_markup=keyboard)

        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши Привет")   

           
        
        elif message.sticker != None:
            if UserMale.male_female!='male' and UserMale.male_female!='female':
                bot.send_message(message.from_user.id, "Укажи кто ты: парень или девушка, чтобы найти себе пару с помощью стикеров")   
            else:
                bot.send_message(message.from_user.id, text='Я начал искать тебе человека, когда найду обязательно напишу')
                user_ID=message.from_user.id
                user_Name=message.from_user.username
                sticker_pack_name=message.sticker.set_name
                user_parameters=[]
                user_parameters.append(user_ID)
                user_parameters.append(user_Name)
                user_parameters.append(sticker_pack_name)  
                user_parameters.append(UserMale.male_female)    

                bot.get_sticker_set(message.sticker.set_name) #получает стикер и выдает его стикер пак
                            #запоминаем данные человека
                Save_user.append(user_parameters)
                columns_for_save_user=['User_ID','User_Name','Sticker_Pack_Name','Sex']
                data=pd.DataFrame(data=Save_user,columns=columns_for_save_user) 
                print(data)
                male=data[data['Sex']=='male']
                female=data[data['Sex']=='female']
                print(male)
                print(female)

                #сравниваем два дата сета мужчин и женщин по стикер паку 
                merge_matrix=pd.merge(male,female, on='Sticker_Pack_Name')
               # print('Вся матрица сравнений:\n',merge_matrix)
                
                
                #сохраняем лог сводной таблицы в файл 
                #file= open("merge_matrix.txt","w")
                #file.write(str(merge_matrix))
                #file.close()
                merge_matrix.to_csv('merge_matrix.csv')
                           
               
                #количество строк массива с найденными одинаковыми значаниями стикер паков
                print('Количество строк в матрице сравнений:\n',len(merge_matrix.index))

                for i in range(len(merge_matrix.index)):
                    if str(user_parameters[3])=='male':
                        if str(user_parameters[0])!=str(merge_matrix.loc[i,'User_ID_x']) and str(merge_matrix.loc[i,'User_ID_y'])!=str(merge_matrix.loc[i,'User_ID_x']): # должно быть !=
                            if str(user_parameters[2])==str(merge_matrix.loc[i,'Sticker_Pack_Name']):
                                bot.send_message(message.from_user.id, 'Я нашел для тебя девушку с такими стикерами, как у тебя') 
                               # a=str(user_parameters[1])
                               # b='@'+a
                                #bot.send_message(message.from_user.id, b)
                                concatination_for_female=str(merge_matrix.loc[i,'User_Name_y'])
                                concatination_for_female_result='@'+concatination_for_female
                                bot.send_message(message.from_user.id, concatination_for_female_result)
                    elif str(user_parameters[3])=='female':
                        if str(user_parameters[0])!=str(merge_matrix.loc[i,'User_ID_y']) and str(merge_matrix.loc[i,'User_ID_y'])!=str(merge_matrix.loc[i,'User_ID_x']):# должно быть !=
                            if str(user_parameters[2])==str(merge_matrix.loc[i,'Sticker_Pack_Name']):
                                bot.send_message(message.from_user.id, 'Я нашел для тебя парня с такими  стикерами, как у тебя') 
                                #a=str(user_parameters[1])
                                #b='@'+a
                                #bot.send_message(message.from_user.id, b)
                                concatination_for_male=str(merge_matrix.loc[i,'User_Name_x'])
                                concatination_for_male_result='@'+concatination_for_male
                                bot.send_message(message.from_user.id, concatination_for_male_result)

        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши - привет")

        # Обработчик нажатий на кнопки
    @bot.callback_query_handler(func=lambda call: True)
    def male_and_female(call):
            # Если нажали на одну из 2 кнопок — выводим просьбу прислать стикер
        if call.data == "Парень": 
                # Пишем сообщение с просьбой о стикере
            msg = "Пришли классный стикер чтобы найти себе пару"
            UserMale.male_female='male'
                # Отправляем текст в Телеграм
            bot.send_message(call.message.chat.id, msg)
               # Получаем стикер сет 
               # bot.get_updates(offset=None, limit=None, timeout=20, allowed_updates=None)     
        elif call.data == "Девушка": 
                # Формируем гороскоп
            msg = 'Пришли классный стикер чтобы найти себе пару'
                # Отправляем текст в Телеграм

            UserMale.male_female='female'
            bot.send_message(call.message.chat.id, msg)  

# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
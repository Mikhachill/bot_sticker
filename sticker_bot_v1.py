import telebot;
import pandas as pd
import numpy as np
import random
from telebot import types
import sqlite3



bot= telebot.TeleBot('1060588156:AAFdHkmHHoiLge3ZGEABmhRAb2SO6_sLGa8');


Save_user=[]
columns_for_save_user=['User_ID','User_Name','Sticker_Pack_Name','Sex']
data=pd.DataFrame(columns=columns_for_save_user)


class UserMale():
    def _init_(self,sex='no male',find=''):
        self.count_for_male=0
        self.sex="no male"
        self.find=find
    
    def male_female(sex):
        return sex
    #Вместо задания глобальных переменных
    def find(type_for_text):
        return type_for_text


    
    @bot.message_handler(content_types=['text','contact', 'sticker'])
    def get_text_messages(message):
        if message.text == "Привет" or message.text == "привет":
            bot.send_message(message.from_user.id, "Привет, хочешь найти себе пару с помощью стикеров")
# Готовим кнопки
            keyboard = types.InlineKeyboardMarkup()
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
                user_parameters=[]
                user_parameters.append(message.from_user.id)
                user_parameters.append(message.from_user.username)
                user_parameters.append(message.sticker.set_name)
                user_parameters.append(UserMale.male_female)
                print(message.from_user.username)
                global data
                
                conn=sqlite3.connect('all_users.db')
                c=conn.cursor()
                param=[(message.from_user.id,message.from_user.username,message.sticker.set_name,UserMale.male_female)]
                c.executemany("INSERT INTO all_users VALUES (?,?,?,?)", param)
                conn.commit()
                conn.close
                
                
                data=pd.read_sql('SELECT * from all_users',conn) 
                
                for i in range(len(data)):# изменяем пол полльзователя во всех данных на пол который пользоавтель указал в текущем сеансе
                    if data['User_Name'][i]==message.from_user.username:
                       #data['Sex'][i]=UserMale.male_female
                        data.loc[i,'Sex']=UserMale.male_female
                
                #'User_ID','User_Name','Sticker_Pack_Name','Sex'

                #нужно сделать один пол для всех вхождений одного пользователя

                print(data)
                
                
                
                male=data[data['Sex']=='male']
                female=data[data['Sex']=='female']
#сливаем (агрегируем) два дата сета мужчин и женщин по стикер паку
                merge_matrix=pd.merge(male,female, on='Sticker_Pack_Name')
                merge_matrix=merge_matrix.drop_duplicates()
                merge_matrix.to_csv('merge_matrix.csv')
                merge_matrix=pd.read_csv('merge_matrix.csv')

                
                merge_matrix=merge_matrix.drop(['Unnamed: 0'],axis=1) #результатом операции drop ялвяются в том числе рваные номера
            #строк поэтому нужно эти номера удалить , что бы можно было прогнать их в массиве
                print('матрица сравнений:\n',merge_matrix)
            
                for i in range(len(merge_matrix.index)):
                    human1=merge_matrix.loc[i,'User_Name_x']
                    human1='@'+str(human1)
                    human2=merge_matrix.loc[i,'User_Name_y']
                    human2='@'+str(human2)
                    if human1 != human2:
                        if merge_matrix.loc[i,'Sex_x'] != merge_matrix.loc[i,'Sex_y']:
                            if human1=='@'+ str(message.from_user.username) and human1 != human2:
                                bot.send_message(message.from_user.id, 'Я нашел для вас партнера')
                                bot.send_message(message.from_user.id, human2)
                            elif human2=='@'+ str(message.from_user.username) and human2 != human1:
                                bot.send_message(message.from_user.id, 'Я нашел для вас партнера')
                                bot.send_message(message.from_user.id, human1)
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши - привет")

# filter on a specific message

 


# Обработчик нажатий на кнопки

    @bot.callback_query_handler(func=lambda call: True)
    def male_and_female(call):
        print('calldata:',call.data)
        if call.data == "Парень":
            msg = "Пришли классный стикер чтобы найти себе пару"
            UserMale.male_female='male'
# Отправляем текст в Телеграм
            bot.send_message(call.message.chat.id, msg)
        elif call.data == "Девушка":
            msg = 'Пришли классный стикер чтобы найти себе пару'
# Отправляем текст в Телеграм
            UserMale.male_female='female'
            bot.send_message(call.message.chat.id, msg)
        
bot.polling(none_stop=True, interval=0)
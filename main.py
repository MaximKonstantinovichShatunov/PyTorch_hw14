import telebot
from telebot import types
from functions import token
import webbrowser
import telebot
from functions import get_object_from_mongodb , insert_data_to_mongodb, check_object_existence, get_collection_count
import datetime

admin_id = 653372350 #5075691809
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['site'])
def get_open_website(message): # Ловит команду "site"       
    webbrowser.open('https://vostok-auto.ru/')



@bot.message_handler(commands=['menu']) # Ловит команду "menu"   
def open_starts(message):
    starts(bot, message)

@bot.message_handler(commands=['start']) # Ловит команду "start"
def registr(message):
    
    def get_firstName(answer):
            reg_list["firstName"] = answer.text
            answer = bot.send_message(message.chat.id, "Введите фамилию:")
            bot.register_next_step_handler(answer, get_lastName)
    def get_lastName(answer):
            reg_list["lastName"] = answer.text
            answer = bot.send_message(message.chat.id, "Введите госномер вашего автомобиля:")
            bot.register_next_step_handler(answer, get_gosNomer)
    def get_gosNomer(answer):
            reg_list["gosNomer"] = answer.text
            answer = bot.send_message(message.chat.id, "Введите номер мобильного телефона:")
            bot.register_next_step_handler(answer, get_phoneNumber)

    def get_phoneNumber(answer):
        number = answer.text
        
        if len(str(number)) >= 10 and ('+' in (str(number)) or '7' in (str(number)) or '8' in (str(number))): # проверка Номера на правильность Написания
            reg_list["phoneNumber"] = answer.text
            bonus = reg_list["bonus"]
            bot.send_message(message.chat.id, f"Спасибо за прохождение регистрации!\n Вам начислено  <b>{bonus}</b> бонусов", parse_mode='html')
            insert_data_to_mongodb(reg_list, "users")
            starts(bot=bot, message=message)
        else:
            bot.send_message(message.chat.id, "Номер телефона должен состоять из <em><b>10 цифр!</b></em>\n Введите номер телефона:", parse_mode='html')
            bot.register_next_step_handler(message, get_lastName)

    if check_object_existence("users", message.from_user.id): # Проверяем, есть ли пользователь в базе данных
        starts(bot=bot, message=message)
    
    else: # если нет, то создаем нового пользователя
        reg_list = {
        "_id" : message.chat.id,
        "firstName" : "",
        "lastName" : "",
        "gosNomer" : "",
        "phoneNumber" : "",
        "bonus" : 1000}
        answer= bot.send_message(message.chat.id, "Здравствуйте. Пожалуйста, зарегистрируйтесь в нашем Боте.\n Введите имя:")

        bot.register_next_step_handler(answer, get_firstName)

def starts(bot, message): 
    """Кнопки главного меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3) # 
    btn1 = types.KeyboardButton("Автосервис🔧")
    btn2 = types.KeyboardButton("Запчасти ⚙️")
    btn3 = types.KeyboardButton(f"Мой  \n профиль")
    btn4 = types.KeyboardButton("Акции\n 💥")
    btn5 = types.KeyboardButton("Перейти на сайт")
    btn6 = types.KeyboardButton("Контакты\n☎️")
    markup.row(btn1, btn2,btn3)
    
    markup.row(btn4,btn5,btn6)
    
    bot.send_message(message.chat.id, f'Добрый день, {message.from_user.first_name}.\nВы в главном меню', reply_markup=markup)
    bot.register_next_step_handler(message, menu_button)
    
    

def menu_button(message):
    
    if message.text == "Автосервис🔧":
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("Замена масла")
        btn2 = types.KeyboardButton("Диагностика")
        btn3 = types.KeyboardButton("Техобслуживание")
        btn4 = types.KeyboardButton("Подвеска")
        btn5 = types.KeyboardButton("Двигатель")
        btn6 = types.KeyboardButton("Тормозная система")
        btn7 = types.KeyboardButton("Трасмиссия")
        btn8 = types.KeyboardButton("Электрооборудование")
        btn9 = types.KeyboardButton("Кондиционер")
        btn10 = types.KeyboardButton("Рулевое управление")
        btn11 = types.KeyboardButton("Выхлопная система")
        btn12 = types.KeyboardButton("Допоборудование")
        markup.row(btn1, btn2,btn3)
        markup.row(btn4,btn5,btn6)
        markup.row(btn7,btn8, btn9)
        markup.row(btn10,btn11, btn12)
        bot.send_message(message.chat.id,f'Выберите услугу',reply_markup=markup)
        bot.register_next_step_handler(message, autoservis_button)

    elif message.text == "Перейти на сайт":        
        webbrowser.open('https://vostok-auto.ru/')
    elif message.text == "Контакты\n☎️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        callback_button = types.KeyboardButton(text="Вернуться в главное меню")
        markup.add(callback_button)
        bot.send_message(message.chat.id,f'<b>Контакты <u>Автосервиса</u> - автосервисы и автозапчасти</b>\n\n'
                         f'+7(831)000-00-00 многоканальный\n'
                         f'+7(929)000-00-00 автосервис\n'
                         f'+7(930)000-00-00 запчасти\n'
                         f'Режим работы: \nПн.-Пт.: с 8-00 до 19-00;\nСб-Вс.: с 9-00 до 18-00', parse_mode='html',reply_markup=markup)
        
    elif message.text == "Мой  \n профиль":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        callback_button = types.KeyboardButton(text="Вернуться в главное меню")
        markup.add(callback_button)
        
        reg_list =get_object_from_mongodb("users", {"_id" : message.from_user.id})
        bot.send_message(message.chat.id,f'<b>Мой профиль</b>\n\n'
                         f'Имя: {reg_list["firstName"]}\n'
                         f'Фамилия: {reg_list["lastName"]}\n'
                         f'Госномер: {reg_list["gosNomer"]}\n'
                         f'Телефон: {reg_list["phoneNumber"]}\n'
                         f'Накоплено бонусов : {reg_list["bonus"]}\n', parse_mode='html',reply_markup=markup)
    
    elif message.text == "Акции\n 💥":
        photo = open('akciya1.jpg', 'rb') 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text ="Записаться на услугу")
        callback_button = types.KeyboardButton(text="Вернуться в главное меню")
        markup.add(btn1,callback_button)
        bot.send_photo(message.chat.id,photo,f'Бесплатная замена масла\nв двигателе'
                                         f' при покупке\n3,5 литров разливного масла\nShell Helix Ultra 5w40 и 5w30.\nВ бесплатный перечень работ входят:\n'
                                        f'- замена масла в двигателе\n- снятие/установка защиты двигателя', parse_mode='markdown',reply_markup=markup)
        bot.register_next_step_handler(message,uslugi_akciya)

def uslugi_akciya(message):
    usluga = "Замена масла В Двигателе(Акция)"
    if message.text == "Записаться на услугу":
        bot.register_next_step_handler(message,zayavka_done,usluga)
    elif message.text == "Вернуться в главное меню":
        starts(bot=bot, message=message)

def autoservis_button(message):
    if message.text == "Замена масла":
        usluga = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("В Двигателе")
        btn2 = types.KeyboardButton("В АКПП")
        callback_button = types.KeyboardButton(text="Вернуться в главное меню")
        markup.add(btn1,btn2,callback_button)
        bot.send_message(message.chat.id,f'Выберите услугу',reply_markup=markup)
        bot.register_next_step_handler(message,Oil_In_Engine,usluga)
        

def Oil_In_Engine(message, usluga):
    if message.text == "Вернуться в главное меню":
        starts(bot=bot, message=message)
    elif message.text == "В Двигателе":
        usluga = usluga + " " + message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton(text ="Записаться на услугу")
        callback_button = types.KeyboardButton(text="Вернуться в главное меню")
        markup.add(btn1,callback_button)
        bot.send_message(message.chat.id,'<b>Замена масла в двигателе</b> <em>500 ₽</em>\n\n<b>Замена масла в двигателе</b><em> 750 ₽</em>\n<em>если клиент предоставит своё масло</em>', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler( message,zayavka_done,usluga)



def zayavka_done( message, usluga):
    if message.text == "Вернуться в главное меню":
        starts(bot=bot, message=message)

    elif message.text == "Записаться на услугу":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        callback_button = types.KeyboardButton(text="Вернуться в главное меню")
        markup.add(callback_button)
        reg_list =get_object_from_mongodb("users", {"_id" : message.from_user.id})
        
        zakaz_id = get_collection_count("zayavki")+100001
        zayavka = {
            "_id" : zakaz_id,
            "firstName" : reg_list["firstName"],
            "phoneNumber" : reg_list["phoneNumber"],
            "usluga" : usluga,
            "time" : datetime.datetime.today().strftime("%d-%b-%Y (%H:%M)")
            }
        
        
            
        bot.send_message(message.chat.id,f'Вашему заказу присвоен номер {zakaz_id}. Заказ отправлен менеджеру.\n'
                            f'Дождитесь обратного звонка в ближайшее время, для уточнения деталей заказа.',reply_markup=markup)
        
        bot.send_message(admin_id, f'!!!ВНИМАНИЕ!!!\n'                                    # Отправка заявки Админу
                                    f'Поступила ЗАЯВКА {zakaz_id}:\n'
                                    f'id чата: {message.chat.id}\n'
                                    f'Имя: {reg_list["firstName"]}\n'
                                    f'Фамилия: {reg_list["lastName"]}\n'
                                    f'Госномер: {reg_list["gosNomer"]}\n'
                                    f'№ телефона: {reg_list["phoneNumber"]}\n'
                                    f'УСЛУГА: {usluga}\n')
        insert_data_to_mongodb(zayavka, "zayavki")
        bot.send_message(admin_id, 'Заявка внесена в базу ✅\n')
            
        
        
            

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Записаться на услугу":
        starts(bot=bot, message=message)
"""
# Дальше Шляпа

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти на сайт", url = 'https://vostok-auto.ru/')
    btn2 = types.InlineKeyboardButton("удалить фото", callback_data='delete')
    btn3 = types.InlineKeyboardButton("изменить текст", callback_data='edit')
    markup.row(btn1)
    markup.row(btn2,btn3)
    bot.reply_to(message, 'Какое красивое фото!',reply_markup = markup)

@bot.message_handler(commands=['start', 'main' , 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'ПРИВЕТ, {message.from_user.first_name}')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>help</b> <em>information</em>', parse_mode='html')
profile_info =5

@bot.callback_query_handler(func=lambda callback: True)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    callback_button = types.KeyboardButton(text="Вернуться в главное меню")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Вернуться в главное меню":
        bot.reply_to(message, "Вы нажали кнопку!")"""






"""def collback_message(callback):


    if callback.data == "Return to top":
        pass
    elif callback.text == "Перейти на сайт\n 🌐":
        webbrowser.open('https://vostok-auto.ru/')
    elif callback.text == "Контакты☎️":
        bot.send_message(callback.chat.id, 'Скоро с вами свяжется наш менеджер')
        bot.register_next_step_handler(callback, autoservis_button)
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
       bot.send_message(message.chat.id, f'ПРИВЕТ, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

def summa(message):
    global amount
    zayavki_col = 5
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, f'не верный формат')
        bot.register_next_step_handler(message, summa)
        return # что бы следующий код не выполнялся
"""
bot.polling(none_stop=True)
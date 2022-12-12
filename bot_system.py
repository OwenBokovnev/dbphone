import telebot
import sqlite3

API_TOKEN = '5892125410:AAESIhsSIMZSWRyH8RhLXdhShZMiFYR7eMs'

bot = telebot.TeleBot(API_TOKEN)

name = ''
surname = ''
phone_number = ''
comments = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'ТЕЛЕФОННЫЙ СПРАВОЧНИК.\n\n1. Просмотреть справочник /show\n2. '
                                      'Добавить телефон /insert\n3. Удалить запись /delete\n\n'
                                      'Так же все мои возможности есть в "Меню"')


@bot.message_handler(commands=['show'])
def get_db_data(message):
    if message.text == '/show':
        connection = sqlite3.connect('dbphone.db')
        cursor = connection.cursor()

        cursor.execute('PRAGMA table_info("dbphone")')
        column_names = [i[1] for i in cursor.fetchall()]

        cursor.execute("SELECT * FROM dbphone")
        rows = cursor.fetchall()

        bot.send_message(message.chat.id, f'Текущая БД: \n{column_names}\n{rows}\n')

        connection.close()


@bot.message_handler(commands=['insert'])
def start(message):
    if message.text == '/insert':
        bot.send_message(message.from_user.id, "Введите ИМЯ: ")
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите ФАМИЛИЮ: ')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Введите НОМЕР ТЕЛЕФОНА: ')
    bot.register_next_step_handler(message, get_phone_number)


def get_phone_number(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id, 'Введите КОММЕНТАРИЙ для номера телефона')
    bot.register_next_step_handler(message, get_comments)
    return phone_number


def get_comments(message):
    global comments
    comments = message.text

    connection = sqlite3.connect('dbphone.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO dbphone VALUES ((SELECT max(id) FROM dbphone) + 1,?,?,?,?)",
                   (surname, name, phone_number, comments))
    connection.commit()
    connection.close()
    bot.send_message(message.chat.id, 'Данные успешно сохранены!\nДля продолжения воспользуйтесь МЕНЮ')
    return comments


@bot.message_handler(commands=['delete'])
def delete_record(message):
    bot.send_message(message.from_user.id, 'Введите ФАМИЛИЮ, которую хотите удалить: ')
    bot.register_next_step_handler(message, delete_record_surname)


def delete_record_surname(message):
    global surname
    surname = message.text
    connection = sqlite3.connect('dbphone.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE from dbphone where surname = ?", (surname, ))
    connection.commit()
    connection.close()
    bot.send_message(message.chat.id, 'Запись удалена!\nДля продолжения воспользуйтесь МЕНЮ')


bot.polling()

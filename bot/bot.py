import telebot
import io
import requests

import analyzer


API_TOKEN = 'token'

bot = telebot.TeleBot(API_TOKEN)

temp_users = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    temp_users[chat_id] = {"data": '', "rate": 0, "start": "", "end": ""}
    txt = 'Привет! Этот бот поможет быстро составить отчет для получения зарплаты, если ты пользуешься "Toggl Tracker"'
    msg = bot.send_message(chat_id, txt)
    txt = '''**Как пользоваться ботом?**\n\
1) Надо перейти по ссылке - https://track.toggl.com/reports\n\
2)В правом верхнем углу будет кнопка "Export"\n\
3)Появится кнопка "Download CSV" - нажать на нее\n\
3)Скинуть этот CSV файл в этот чат\n\
4)Готово!
    '''
    msg = bot.send_message(chat_id, txt)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    file_ext = message.document.file_name.split('.')[-1]

    if file_ext.lower() == 'csv':
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
        response = requests.get(file_url)
        csv_content = response.content.decode('utf-8')
        csv_file = io.StringIO(csv_content)
        data = analyzer.get_stat(csv_file)
        temp_users[chat_id]['data'] = data
        msg = bot.send_message(chat_id, "Введите часовую ставку в рублях")
        # txt = analyzer.get_text(data,300,'09.01','12.02')
        # analyzer.get_pie(data)
        # bot.send_message(chat_id, txt)
    else:
        bot.send_message(chat_id, "Это не csv файл. Попробуйте снова")

    bot.register_next_step_handler(msg, get_rate)

def get_rate(message):
    chat_id = message.chat.id
    temp_users[chat_id]['rate'] = int(message.text)
    msg = bot.send_message(chat_id, 'Введите начало отчетного периода в формате "ДД.ММ"')
    bot.register_next_step_handler(msg, get_start_per)


def get_start_per(message):
    chat_id = message.chat.id
    temp_users[chat_id]['start'] = message.text
    msg = bot.send_message(chat_id, 'Введите конец отчетного периода в формате "ДД.ММ"')
    bot.register_next_step_handler(msg, get_end_per)

def get_end_per(message):
    chat_id = message.chat.id
    temp_users[chat_id]['end'] = message.text
    data = temp_users[chat_id]['data']
    rate = temp_users[chat_id]['rate']
    start = temp_users[chat_id]['start']
    end = temp_users[chat_id]['end']
    txt = analyzer.get_text(data, rate, start, end)
    analyzer.get_pie(data)
    bot.send_message(chat_id, txt)
    bot.send_photo(chat_id, photo=analyzer.get_pie(data))

bot.infinity_polling()
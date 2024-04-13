import telebot
from collect_feature_for_new_coordinates import return_index


bot = telebot.TeleBot('6726785116:AAEdAtOEv1KRKIBsoSYy_LPo5ROgrNO5qh8')


@bot.message_handler(commands=['start'])
def start(message):
    mess = '''Привет! 
Этот бот расчитывает индекс популярности геолокации для размещения банкомата на территории РФ. 
Введи через пробел широту долготу и группу банкоматов, например: 
46.937353 142.753348 32'''
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler()
def get_message(message):
    if len(message.text.split())==3:
        text = message.text.split()
        try:
            text = list(map(float, text))
            bot.send_message(message.chat.id, 'Пожалуйста, подожди 3-4 минуты для получения результата', parse_mode='html')
            lat = text[0]
            lon = text[1]
            atm_group = text[2]
            index = return_index(lat, lon, atm_group)
            bot.send_message(message.chat.id, 'Индекс популярности для заданных координат составляет '+str(index), parse_mode='html')
        except:
            bot.send_message(message.chat.id, 'Что то пошло не так. Попробуй еще раз', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так. Попробуй еще раз', parse_mode='html')


bot.polling(none_stop = True)

















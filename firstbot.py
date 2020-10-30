import telebot
import config
from telebot import types


bot = telebot.TeleBot(config.API_TOKEN)


# Handle '/start' and '/help'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, "+ message.chat.first_name +"! Меня зовут {}!".format(bot.get_me().username))
    #keyboard
    btnOk = types.InlineKeyboardButton("Хорошо", callback_data='good')
    btnBad = types.InlineKeyboardButton("Замечательно!", callback_data='exciting')
    markup = types.InlineKeyboardMarkup()
    markup.add(btnOk, btnBad)
    bot.send_message(message.chat.id, "Как дела?", reply_markup=markup)
	


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def send_answer(message):
	if message.text == 'Привет':
		bot.send_message(message.chat.id, "Снова здравствуй, {}!".format(message.chat.first_name))
	elif message.text == 'Как дела?':
		bot.send_message(message.chat.id, "Нормально! Как у тебя?")
	else:
		bot.send_message(message.chat.id, "Извини, {}. Я пока только учусь, поэтому не могу еще ответить тебе на это :(".format(message.chat.first_name))
    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Это замечательная новость!')
                bot.send_message('@MyBotAnswer', '1')
            elif call.data == 'exciting':
                bot.send_message(call.message.chat.id, 'Я просто в восторге от этого!!!')
                bot.send_message('@MyBotAnswer', '2')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела?",
                reply_markup=None)
 
            # show alert
            #bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #    text="This is a test message!!!")
 
    except Exception as e:
        print(repr(e))
	

bot.polling(none_stop=True)
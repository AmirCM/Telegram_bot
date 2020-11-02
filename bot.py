import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext


def echo(update, context):
    if update.effective_chat.type == 'channel':
        print(update)
        print(update['channel_post'])
        print(update['channel_post']['chat'])
        print(update.effective_chat)
    else:
        print(update.effective_chat)
        print('*** PV msm ***')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Amir's bot, please talk to me!"
                                                                    "\n$=27750, EUR=32646, GBP=37509")


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    print(text_caps)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update, context: CallbackContext):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


with open('config.txt', 'r') as conf:
    token = conf.readline()
    conf.close()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=token)
dispatcher = updater.dispatcher

echo_handler = MessageHandler(Filters.all, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()

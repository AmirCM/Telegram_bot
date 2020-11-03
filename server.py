import logging

from telegram import Update
from telegram.ext import *
from main import Currency

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

started = False
message = None
f = False
c = Currency()


def post_reporter():
    global f
    post_text = ['📉 دلار', '📉 یورو', '📉 پوند انگلیس']
    sell = '👈 نرخ فروش: '
    buy = '👈🏼 خرید از مشتری: '
    c.update_db()
    text = ''
    for i, p in enumerate(post_text):
        text += p + '\n' + sell + str(c.price[i]) + '\n' + buy + str(int(c.price[i] * 0.99)) + '\n-------------------\n'
    if f:
        f = False
        return text + '\n @testerr'
    else:
        f = True
        return text + '\n @tester'


def alarm(context: CallbackContext):
    global message
    c.update_db()
    context.bot.editMessageText(post_reporter(), message['chat']['id'], message['message_id'])


def all_msm(update: Update, context: CallbackContext) -> None:
    # print(context.bot.editMessageText())
    print(update.effective_chat)
    print(update)


def start_updating(update: Update, context: CallbackContext) -> None:
    global started, message
    if update.effective_chat.type == 'channel':
        if update['channel_post']['text'] == '/st_up':
            started = True
            message = update['channel_post']
            print(message)
            print('started')
            context.bot.editMessageText(post_reporter(), message['chat']['id'], message['message_id'])
            context.job_queue.run_repeating(alarm, 60)


with open('config.txt', 'r') as conf:
    token = conf.readline()
    conf.close()

updater = Updater(token)
dispatcher = updater.dispatcher

# on different commands - answer in Telegram
dispatcher.add_handler(MessageHandler(Filters.command, start_updating))
dispatcher.add_handler(MessageHandler(Filters.text, all_msm))

# Start the Bot
updater.start_polling()
updater.idle()

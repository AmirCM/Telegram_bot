import logging
from builtins import print

from telegram import Update
from telegram.ext import *
from main import Currency

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

started = False
message_id = ''
chat_id = ''
f = False
c = Currency()


def post_reporter():
    global f
    post_text = ['📉 دلار', '📉 یورو', '📉 پوند انگلیس']
    sell = '👈 نرخ فروش: '
    buy = '👈🏼 خرید از مشتری: '
    c_prices = c.update_db()
    rials = c.to_rial(c_prices.copy())
    rials = {k: v for k, v in sorted(rials.items(), key=lambda item: item[1], reverse=True)}
    text = ''
    for i, p in enumerate(post_text):
        text += p + '\n' + sell + str(c.price[i]) + '\n' + buy + str(int(c.price[i] * 0.99)) + '\n\n'

    text += '📌نرخ بروز ارزهای دیجیتال: '
    text += '\nــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'

    emoji = '📉'
    for k, v in rials.items():
        text += emoji + ' نرخ ' + c_prices[k] + ' : ' + k + '\n' + sell + str(v) + '\n' + buy + str(
            int(v * 0.99)) + '\n\n'

    return text + '\n @keep_exchange \n'


def alarm(context: CallbackContext):
    global chat_id
    txt = ''
    try:
        txt = post_reporter()
        print(txt)
        context.bot.send_message(chat_id, txt)
    except:
        print('ERROR')
        context.bot.send_message(chat_id, txt)


def all_msm(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat)
    print(update)


def command_handler(update: Update, context: CallbackContext) -> None:
    global started, message_id, chat_id
    if update.effective_chat.type == 'channel':
        if update['channel_post']['text'] == '/st_up079' and started is False:
            started = True
            msg = update['channel_post']
            print(msg)
            message_id = msg['message_id']
            chat_id = msg['chat']['id']
            print('started')
            context.bot.editMessageText(post_reporter(), chat_id, message_id)
            context.job_queue.run_repeating(alarm, 60)
        elif update['channel_post']['text'] == '/resetup' and started:
            started = False
            msg = update['channel_post']
            print(msg)
            message_id = msg['message_id']
            chat_id = msg['chat']['id']
            context.bot.delete_message(chat_id, message_id)


with open('config.txt', 'r') as conf:
    token = conf.readline()
    conf.close()

updater = Updater(token)
dispatcher = updater.dispatcher

# on different commands - answer in Telegram
dispatcher.add_handler(MessageHandler(Filters.command, command_handler))
dispatcher.add_handler(MessageHandler(Filters.text, all_msm))

# Start the Bot
updater.start_polling()
updater.idle()

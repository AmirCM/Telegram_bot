import logging
from builtins import print
import jdatetime
from telegram import Update
from telegram.ext import *
from main import Currency
from unidecode import unidecode

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


def separator(p: str):
    i = 3 - len(p) % 3
    rs = ''
    for j, ch in enumerate(p):
        if (j + i) % 3 == 0 and j != 0:
            rs += ',' + ch
        else:
            rs += ch
    return rs


def post_reporter():
    global f

    persian = {'BTC': 'بیت‌کوین (BTC)‏',
               'ETH': 'اتریوم (ETH)‏ ',
               'XMR': ' مونرو (XMR)‏ ',
               'DASH': ' دش (DASH)‏ ',
               'LTC': 'لایت کوین (LTC)‏ ',
               'USDT': ' تتر (USDT)‏ ',
               'ADA': 'کاردانو (ADA)‏ ',
               'TRX': ' ترون (TRX)‏ '}

    post_text = ['📉 دلار', '📉 یورو', '📉 پوند انگلیس']
    sell = '👈 نرخ فروش: '
    buy = '👈🏼 خرید از مشتری: '
    c_prices = c.update_db()
    rials = c.to_rial(c_prices.copy())

    rials = {k: v for k, v in sorted(rials.items(), key=lambda item: item[1], reverse=True)}

    x = jdatetime.datetime.now()
    text = '📅 تاریخ: ' + x.strftime('%x') + '\n' + '⏰ ساعت: ' + x.strftime('%X') + '\n'
    for i, p in enumerate(post_text):
        text += p + '\n' + sell + separator(str(c.price[i])) + '\n' + buy + \
                separator(str(int(c.price[i] * 0.99))) + '\n\n'

    text += '📌نرخ بروز ارزهای دیجیتال: '
    text += '\nــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'

    emoji = '📉'
    for k, v in rials.items():
        text += emoji + '\t' + persian[k] + ':'
        text += str(round(float(c_prices[k]), 3)) + '$' + '\n'
        text += sell + separator(str(v)) + '\n'
        text += buy + separator(str(int(v * 0.99))) + '\n\n'

    return text + '\n @keep_exchange \n'


def alarm(context: CallbackContext):
    global chat_id
    try:
        txt = post_reporter()
        context.bot.send_message(chat_id, txt)
    except:
        print('ERROR')


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
            context.job_queue.run_repeating(alarm, 120)
        elif update['channel_post']['text'] == '/resetup$' and started:
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

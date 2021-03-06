import logging
from builtins import print
import jdatetime
import time
from telegram import Update
from telegram.ext import *
from main import Currency
from unidecode import unidecode
import pytz

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
counter = 0


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
    print('Reporting started')
    tic = time.perf_counter()
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
    tz = pytz.timezone('Iran')
    x = jdatetime.datetime.now(tz)
    text = '📅 تاریخ: ' + x.strftime('%Y/%-m/%-d') + '\n' + '⏰ ساعت: ' + x.strftime('%X') + '\n'
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
    print('Reporting elapse time {:.2f}'.format(time.perf_counter() - tic))
    return text + '\n @keep_exchange \n'


def alarm(context: CallbackContext):
    print('Instance {} is running'.format(context.job))
    global counter
    counter += 1
    print('Handler: {}'.format(counter))
    global chat_id
    try:
        txt = post_reporter()
        context.bot.send_message(chat_id, txt)
    except:
        print('ERROR')
    print('Instance {} is ended'.format(context.job))


def all_msm(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat)
    print(update)


def command_handler(update: Update, context: CallbackContext) -> None:
    global started, message_id, chat_id
    text = update['channel_post']['text']
    msg = update['channel_post']
    if update.effective_chat.type == 'channel' and update.effective_chat.username == 'keep_exchange':
        if (text == '/st_upT60' or text == '/st_upT300') and started is False:
            started = True
            message_id = msg['message_id']
            chat_id = msg['chat']['id']
            print('Started')
            context.bot.editMessageText(post_reporter(), chat_id, message_id)
            t = int(text.split('T')[1])
            print(t)
            context.job_queue.run_repeating(alarm, t)
        elif update['channel_post']['text'] == '/resetup$' and started:
            started = False
            message_id = msg['message_id']
            chat_id = msg['chat']['id']
            context.bot.delete_message(chat_id, message_id)
            context.job_queue.stop()
            print('Stopped')


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

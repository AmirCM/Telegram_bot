import logging

from telegram import Update
from telegram.ext import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

started = False
message = None
i = 0


def alarm(context: CallbackContext):
    """Send the alarm message."""
    global i, message
    i += 1
    print(context)
    context.bot.editMessageText('Beep! ' + str(i), message['chat']['id'], message['message_id'])


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
            context.bot.editMessageText('BEEP@!@!', message['chat']['id'], message['message_id'])
            context.job_queue.run_repeating(alarm, 5)


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

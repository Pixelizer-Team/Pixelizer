import telegram
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


with open('Token.txt', 'r') as confidential:
    our_secret_token = confidential.readline()

examples = {
    'cube': 'samples/cube/scream_5.jpg',
    'dcube': 'samples/dcube/gogh_15.jpg',
    'vor': 'samples/vor/mona_1000.jpg',
    'hex': 'samples/hex/hex_15.jpg',
    'wall': 'samples/wall/green_30.jpg',
    'sq': 'samples/sq/monroe_20.jpg',
    'split': 'samples/split/split_23.jpg',
}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Welcome to Pixelizer!\n'
                              'In an era in which resolution has become overrated by diverse propagandas, we strike by redefining our pixels!')
    bot = context.bot
    # telegram.Bot.send_photo(our_secret_token, photo=examples['cube'])
    bot.send_photo(chat_id=update.message.chat_id, photo=open(examples['cube'], 'rb'))


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('We are alone in this dark dark world, May God bless thy soul...')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def curse(update, context):
    update.message.reply_text('We politely request that you stop fucking around with our bot')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(our_secret_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, curse))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

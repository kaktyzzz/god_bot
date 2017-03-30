# -*- coding: utf-8 -*-
import config
import flask
from time import sleep
import bot

app = flask.Flask(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

# Process webhook calls
@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = bot.telebot.types.Update.de_json(json_string)
        bot.bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.bot.remove_webhook()
sleep(2)

# Set webhook
bot.bot.set_webhook(url=config.WEBHOOK_URL_BASE+config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=config.WEBHOOK_LISTEN,
        port=config.WEBHOOK_PORT,
        ssl_context=(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV),
        debug=True)


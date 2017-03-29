import bot
from time import sleep

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.bot.remove_webhook()
sleep(5)
bot.bot.polling()

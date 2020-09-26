import logging
import os
import telegram
from telegram import MessageEntity
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters
import pyshorteners

logging.basicConfig(
    level=logging.INFO,
    format ="%(asctime)s - %(name)s - %(levelname)s - %(message)s, "
)
logger = logging.getLogger()

TOKEN = "1184851528:AAE_5plWfrsxuqk8xf262cya26w8cb6YM3Y"

def start(update,context):
    print(update.effective_user)
    nombre = update.effective_user['first_name']
    logger.info(f"El usuario {nombre} se ha conectado")
    update.message.reply_text(f"Bienvenido, {nombre}")

def url_shortener(update,context):
    id = update.effective_user["id"]
    logger.info(f"El usuario {id} ha enviado un enlace")
    texto = update.message.text
    shortener = pyshorteners.Shortener()
    nueva_url = shortener.tinyurl.short(texto)

    context.bot.sendMessage(
        chat_id = id,
        parse_mode ="HTML",
        text = f"<b> Tu URL reducida es: </b> {nueva_url}"
    )

def validar (update,context):
    id = update.effective_user["id"]
    nombre = update.effective_user["first_name"]
    logger.info(f"El usuario {id} ha enviado un texto")
    context.bot.sendMessage(
        chat_id = id,
        parse_mode ="HTML",
        text = f"Hola {nombre}. Solo recibimos URLs por el momentoclea"
    )
    
    

if __name__ == "__main__":

    url_bot = telegram.Bot(token= TOKEN)
    #Obtener información
    print(url_bot.getMe())
    #Enlaza nuestro bot al updater
    updater = Updater(url_bot.token, use_context=True)
    #Crea despachador
    dp = updater.dispatcher
    #Crear gestor de acciones del Bot
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(MessageHandler(Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK),url_shortener))
    dp.add_handler(MessageHandler(Filters.text,validar))

    #Monitoreo de manera constante si existe o no mensajes
    updater.start_polling()

    #Ctrl + C para finalizar el proceso
    updater.idle()
    












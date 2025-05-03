import telebot
from dotenv import load_dotenv

from Globais import Globais
import os

load_dotenv()
chave_api_telegram = os.getenv('CHAVE_API_TELEGRAM')

#Criacao do Bot
Globais.bot = telebot.TeleBot(chave_api_telegram)
bot = Globais.bot


#Looping para o bot ficar rodando
bot.polling()
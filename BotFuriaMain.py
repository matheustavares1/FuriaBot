import telebot
from dotenv import load_dotenv

from Globais import Globais
import os


load_dotenv()
chave_api_telegram = os.getenv('CHAVE_API_TELEGRAM')

#Criacao do Bot
Globais.bot = telebot.TeleBot(chave_api_telegram)
bot = Globais.bot


from Menu.Menus import pedir_nome, funcao_inicio
from Quiz.QuizLogica import mensagem_inicial_quiz, iniciar_quiz, sair_quiz, processar_resposta




#Funcionalidade /quiz sair do quiz e correcao de respostas
bot.message_handler(commands=['quiz'])(lambda msg: mensagem_inicial_quiz(msg))
bot.message_handler(commands=['iniciar_quiz'])(lambda msg: iniciar_quiz(msg))
bot.message_handler(commands=['sair_quiz'])(lambda msg: sair_quiz(msg))
bot.callback_query_handler(func=lambda call: True)(lambda call: processar_resposta (call))
#Pedir nome do usuario
bot.message_handler(commands=['iniciar'])(lambda msg: pedir_nome( msg))

#Funcao para mandar mensagem inicial
bot.message_handler(func=lambda msg: True)(lambda msg: funcao_inicio( msg))
bot.delete_webhook()
#Looping para o bot ficar rodando
bot.polling()
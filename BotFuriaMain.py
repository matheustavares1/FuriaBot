import threading

import telebot
from dotenv import load_dotenv

from Globais import Globais
import os


load_dotenv()
chave_api_telegram = os.getenv('CHAVE_API_TELEGRAM')

#Criacao do Bot
Globais.bot = telebot.TeleBot(chave_api_telegram)
bot = Globais.bot

from Campeonato.ProximoCampeonato import proximo_campeonato_handler
from Curiosidades.CuriosidadesLogic import chamar_curiosidades
from Elenco.Elenco import elenco_atual
from Menu.Menus import pedir_nome, funcao_inicio
from Quiz.QuizLogica import mensagem_inicial_quiz, iniciar_quiz, sair_quiz, processar_resposta
from NotificacoesNoticias.NoticiasLogica import ultimas_noticias
from NotificacoesNoticias.NotificacoesLogica import ativar_noticias, desativar_noticias, monitorar_noticias
from Historico.HistoricoLogica import historico_jogos


#Funcao que lista elenco atual da FURIA
bot.message_handler(commands=['elenco_atual'])(lambda msg: elenco_atual(bot, msg))

#Funcao de curiosodades da furia
bot.message_handler(commands=['curiosidades'])(lambda msg: chamar_curiosidades(bot, msg))

#Funcionalidade /quiz sair do quiz e correcao de respostas
bot.message_handler(commands=['quiz'])(lambda msg: mensagem_inicial_quiz(msg))
bot.message_handler(commands=['iniciar_quiz'])(lambda msg: iniciar_quiz(msg))
bot.message_handler(commands=['sair_quiz'])(lambda msg: sair_quiz(msg))
bot.callback_query_handler(func=lambda call: True)(lambda call: processar_resposta (call))

#Funcao para puxar o historico dos ultimos jogos
bot.message_handler(commands=['historico_de_jogos'])(lambda msg: historico_jogos( msg))

#Proximo campeonato da FURIA CS
bot.message_handler(commands=['proximo_campeonato'])(lambda msg: proximo_campeonato_handler(msg))

#Funcao para ultimas noticias do mundo do EaSports
bot.message_handler(commands=['ultimas_noticias'])(lambda msg: ultimas_noticias(bot, msg))

#Ativar noticias automaticas
bot.message_handler(commands=['receber_noticias'])(lambda msg: ativar_noticias( msg))

#Cancelar notiticas automaticas
bot.message_handler(commands=['parar_noticias'])(lambda msg: desativar_noticias(msg))


#Pedir nome do usuario
bot.message_handler(commands=['iniciar'])(lambda msg: pedir_nome( msg))

#Funcao para mandar mensagem inicial
bot.message_handler(func=lambda msg: True)(lambda msg: funcao_inicio( msg))



threading.Thread(target=monitorar_noticias, daemon=True).start()
bot.delete_webhook()
#Looping para o bot ficar rodando
bot.polling()

import json
import time

from NotificacoesNoticias.NoticiasLogica import scraping_ultimas_noticias
from Globais.Globais import *

ARQUIVO_NOTIFICACOES = "usuarios_notificados.json"

def carregar_usuarios():
    try:
        with open(ARQUIVO_NOTIFICACOES, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_usuarios(lista):
    with open(ARQUIVO_NOTIFICACOES, "w") as f:
        json.dump(lista, f)

def adicionar_usuario(user_id):
    usuarios = carregar_usuarios()
    if user_id not in usuarios:
        usuarios.append(user_id)
        salvar_usuarios(usuarios)

def remover_usuario(user_id):
    usuarios = carregar_usuarios()
    if user_id in usuarios:
        usuarios.remove(user_id)
        salvar_usuarios(usuarios)

ultima_noticia_enviada = ""
def monitorar_noticias():
    global ultima_noticia_enviada
    while True:
        titulo_noticia, link = scraping_ultimas_noticias()
        if titulo_noticia != ultima_noticia_enviada:
            ultima_noticia_enviada = titulo_noticia
            mensagem = f"🆕 *Nova notícia EA SPORTS!*\n\n*{titulo_noticia}*\n\n👉 Leia mais: {link}"
            for user_id in carregar_usuarios():
                bot.send_message(user_id, mensagem, parse_mode='Markdown')
        time.sleep(600)  # verifica a cada 10 minutos


def ativar_noticias(message):
    user_id = message.from_user.id
    adicionar_usuario(user_id)
    bot.reply_to(message, "🔔 Você se inscreveu para receber notificações de novas notícias EA SPORTS!\n\n"
                           "🚫 Para cancelar a inscrição digite/clique: /parar_noticias")

def desativar_noticias( message):
    user_id = message.from_user.id
    remover_usuario(user_id)
    bot.reply_to(message, "🚫 Você não receberá mais notificações de notícias.")

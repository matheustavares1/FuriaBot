from Globais.Globais import *
from Quiz.QuizLogica import mensagem_inicial_quiz


def pedir_nome(message):
    user_id = message.from_user.id
    if user_id not in nome_usuario:
        bot.reply_to(message, "👋 Antes de começarmos, digite como gostaria de ser chamado?")
        bot.register_next_step_handler(message, salvar_nome)
    else:
        enviar_menu(message)

def salvar_nome(message):
    user_id = message.from_user.id
    nome = message.text.strip()
    nome_usuario[user_id] = nome  # Armazena o nome
    bot.reply_to(message, f"Show, {nome}! 🔥 Vamos nessa!\n")
    enviar_menu(message)


def enviar_menu(message):
    nome = nome_usuario.get(message.from_user.id, "Furioso(a)")
    texto_menu = (
           f"<b>🔥 Bem-vindo ao hub oficial da FURIA, {nome}! 🔥</b>\n\n"
    "Aqui você encontra tudo sobre a maior organização de eSports do Brasil!\n"
    "Escolha uma das opções abaixo e fique por dentro do mundo da <b>FURIA</b>! 💥\n\n"
    "📅 <b>/historico_de_jogos</b> — Reviva as batalhas passadas da equipe!\n"
    "👥 <b>/elenco_atual</b> — Conheça os jogadores que vestem o manto da FURIA!\n"
    "🔍 <b>/curiosidades</b> — Descubra fatos e histórias que você (provavelmente) não sabia!\n"
    "🧠 <b>/quiz</b> — Prove que é um verdadeiro fã da FURIA!\n"
    "📰 <b>/ultimas_noticias</b> — Fique ligado nas novidades quentinhas!\n"
    "🏆 <b>/proximo_campeonato</b> — Saiba onde e quando será a próxima disputa da FURIA no CS2!\n"
    )

    bot.reply_to(message, texto_menu , parse_mode='html')



def funcao_inicio(message):
    user_id = message.from_user.id
    if user_id not in nome_usuario:
        bot.reply_to(message, "🖤🐾Fala, furioso(a)! Bem vindo(a) ao bot da FURIA!🖤🐾\n\n"
                            "🔥 Aqui você tem informações rápidas e interessantes sobre o time de CS2 mais insano do Brasil, além de ficar por dentro das últimas notícias que rolam no mundo do EA-SPORTS. Quer ficar por dentro?\n"
                            "Entao vem com a gente! 🖤 \n\n"
                            "Digite/clique o comando /iniciar para começarmos essa aventura FURIOSA!🔥")
        return

    if user_id in usuarios_quiz:
        enviar_menu(message)
    else:
        mensagem_inicial_quiz(message)


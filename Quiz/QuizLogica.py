from telebot import types
from Globais.Globais import *
from Quiz.QuizPerguntas import perguntas_quiz, TOTAL_PERGUNTAS

pontuacao_anterior = {}


def mensagem_inicial_quiz(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    nome = nome_usuario.get(user_id, "Furioso(a)")
    ultima_pontuacao = pontuacao_anterior.get(chat_id, 0)
    resposta = (f"🖤🐾 Faaala {nome}!! Esse é o quiz da FURIA, está preparado(a) para testar seus conhecimentos sobre o melhor time de CS2 do mundo?\n\n"
                f"🔍 Serao 10 perguntas com 4 alternatinas e apenas 1 correta.\n"
                f"🧠 Para comecar cliquem em: /iniciar_quiz \n"
                f"❌ Caso queria sair do quiz use o comando: /sair_quiz\n\n"
                f"📊 Sua última pontuação foi: {ultima_pontuacao}/{TOTAL_PERGUNTAS}")

    bot.send_message(user_id, resposta, parse_mode='html')

def iniciar_quiz( message):
    chat_id = message.chat.id
    usuarios_quiz[chat_id] = {'idx': 1, 'score': 0}

    enviar_pergunta(chat_id)

def sair_quiz( message):
    chat_id = message.chat.id
    if chat_id in usuarios_quiz:
        usuarios_quiz.pop(chat_id)
        bot.reply_to(message, '🚶‍♂️ Quiz encerrado. Até a próxima!')
        bot.delete_message(chat_id, message.message_id)
    else:
        bot.reply_to(message, '⚠️ Você não está em um quiz agora.')

def enviar_pergunta( chat_id):
    estado = usuarios_quiz[chat_id]
    info = perguntas_quiz[estado['idx']]
    markup = types.InlineKeyboardMarkup()
    for opc in info['opcoes']:
        markup.add(types.InlineKeyboardButton(opc, callback_data=opc))
    bot.send_message(chat_id, info['pergunta'], reply_markup=markup)

def processar_resposta( call):
    chat_id = call.message.chat.id
    if chat_id not in usuarios_quiz:
        return bot.answer_callback_query(call.id, 'Você não está no quiz.')
    estado = usuarios_quiz[chat_id]
    info = perguntas_quiz[estado['idx']]
    # desabilitar botões
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    # verificar resposta
    if call.data.lower() == info['resposta_correta'].lower():
        estado['score'] += 1
        bot.send_message(chat_id, '✅ Acertou!')
    else:
        bot.send_message(chat_id, f"❌ Errou! Resposta certa: *{info['resposta_correta']}*", parse_mode='Markdown')
    # próxima
    estado['idx'] += 1
    if estado['idx'] > TOTAL_PERGUNTAS:
        bot.send_message(chat_id,
            f"🏁 Quiz finalizado! Você acertou {estado['score']} de {TOTAL_PERGUNTAS}.")
        #salvar pontucao
        pontuacao_anterior[chat_id] = estado['score']
    else:
        enviar_pergunta( chat_id)
    bot.answer_callback_query(call.id)
import random

from Curiosidades.CuriosidadeDados import curiosidades

def chamar_curiosidades(bot ,message):
    curiosidade = random.choice(curiosidades)
    bot.reply_to(message, curiosidade, parse_mode='Markdown')

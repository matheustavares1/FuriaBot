from Elenco.ElencoDados import *


def formatar_elenco():
    lines = [
        "<b>📋 Elenco Atual da FURIA (abril de 2025):</b>\n"
    ]
    lines.append("<b>🎯 Titulares:</b>")
    for p in TITULARES:
        lines.append(f"👤 <b>{p['nickname']}</b> ({p['name']}) - {p['role']}")
    lines.append("\n<b>🧩 Reservas:</b>")
    for p in RESERVAS:
        lines.append(f"👤 <b>{p['nickname']}</b> ({p['name']}) - {p['role']}")
    lines.append("\n<b>🧠 Comissão Técnica:</b>")
    for p in COMISSAO_TECNICA:
        lines.append(f"👤 <b>{p['nickname']}</b> ({p['name']}) - {p['role']}")
    return "\n".join(lines)


def elenco_atual(bot, message):
    texto = formatar_elenco()
    bot.reply_to(message, texto, parse_mode='html')

import requests
from bs4 import BeautifulSoup

from Globais.Globais import nome_usuario


#Scraping
def scraping_ultimas_noticias():
    # Requisicao GET
    response = requests.get("https://www.dust2.com.br/")
    # Verificar requisicao
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar o site. Status code: {response.status_code}")

    # Parsing do conteudo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscando titulo da noticia
    titulo_noticia = soup.find('div', class_='news-item-header')
    if not titulo_noticia:
        raise Exception("Título da notícia não encontrado.")

    # Pegando o link da noticia
    link_noticia = soup.find('a', class_='a-block standard-box news-item big-article')
    if not link_noticia:
        raise Exception("Link da notícia não encontrado.")

    link = link_noticia["href"]

    return titulo_noticia.text.strip(), f"https://www.dust2.com.br{link}"


def formatar_noticia():
    try:
        titulo_noticia, link = scraping_ultimas_noticias()
        resposta = (
            "📰 *Última notícia sobre o mundo EA SPORTS:*\n\n"
            f"*{titulo_noticia}*\n\n"
            f"👉 Leia mais: {link}\n\n"
            "🔔 Ative o recebimento automático de notícias com /receber_noticias 🔔"
        )
    except Exception as e:
        texto = f"❌ Não foi possível buscar a última notícia:\n{e}"
    return resposta


def ultimas_noticias(bot,message):
    nome = nome_usuario.get(message.from_user.id, 'Furioso(a)')
    bot.reply_to(message, f'Eai {nome}! 🔥 Estamos bucando as últimas notícias para voce ficar 100% atualziado! 📅')
    bot.reply_to(message, formatar_noticia(), parse_mode='html')

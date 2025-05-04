from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Globais.Globais import *


def proximo_campeonato():
    # Configurações para rodar o Chromium em modo Headless
    options = Options()
    #options.add_argument("--headless")  # Modo sem interface gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
   # service = Service("/usr/local/bin/chromedriver")
    # Configurar o WebDriver com o caminho do driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://draft5.gg/equipe/330-FURIA/campeonatos')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    titulo = soup.find('h4', class_='TournamentCard__TournamentCardDescriptionTitle-sc-1vb6wff-2 eGbvbu').text.strip()
    data = soup.find('small', class_='TournamentCard__TournamentCardDescriptionDate-sc-1vb6wff-3 fKZACE').text.strip()
    link_classe = soup.find('a', class_='TournamentCard__TournamentCardContainer-sc-1vb6wff-0 TaBXn TournamentList__StyledTournamentCard-sc-10easx8-0 lmkAmS')
    link = link_classe.get('href')
    campeonato =[titulo, data, link]

    return campeonato




 #Formatar dados do próximo campeonato
def formatar_mensagem_campeonato(campeonato):
    titulo, data, link = campeonato
    mensagem = f"""
 🏆 *Próximo Campeonato da FURIA* 🔥

 📌 *Campeonato:* {titulo}
 🗓 *Data:* {data}
 🔗 *Link:* [Clique aqui para mais detalhes](https://draft5.gg{link})
     """
    return mensagem

# Buscar dados e enviar ao usuário
def proximo_campeonato_handler(message):
    nome = nome_usuario.get(message.from_user.id, 'Furioso(a)')
    bot.reply_to(message, f"Fala {nome}! 🏆 Buscando o próximo campeonato da FURIA pra você...")

    try:
        campeonato = proximo_campeonato()  # Função que usa Selenium
        mensagem_resposta = formatar_mensagem_campeonato(campeonato)
    except Exception as error:
        mensagem_resposta = "❌ Ocorreu um erro ao buscar os dados. Tente novamente mais tarde."
        print(f"[Erro Selenium] {error}")

    bot.reply_to(message, mensagem_resposta, parse_mode='Markdown')
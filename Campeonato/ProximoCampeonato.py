
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Globais.Globais import *
import tempfile

def proximo_campeonato():
    # Configurações para rodar o Chromium em modo Headless
    options = Options()
    options.add_argument("--headless")  # Modo sem interface gráfica
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={temp_dir}')

    # Configurar o WebDriver com o caminho do driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://draft5.gg/equipe/330-FURIA/campeonatos')

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    wait = WebDriverWait(driver, 10)
    # Espera até que o título do próximo campeonato esteja presente
    titulo_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'TournamentCard__TournamentCardDescriptionTitle-sc-1vb6wff-2'))
    )
    titulo = titulo_element.text.strip()

    # Espera até que a data do próximo campeonato esteja presente
    data_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'TournamentCard__TournamentCardDescriptionDate-sc-1vb6wff-3'))
    )
    data = data_element.text.strip()

    # Espera até que o link do próximo campeonato esteja presente
    link_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'TournamentCard__TournamentCardContainer-sc-1vb6wff-0'))
    )
    link = link_element.get_attribute('href')
    campeonato =[titulo, data, link]

    return campeonato


 #Formatar dados do próximo campeonato
def formatar_mensagem_campeonato(campeonato):
    titulo, data, link = campeonato
    mensagem = f"""
 🏆 *Próximo Campeonato da FURIA* 🔥

 📌 *Campeonato:* {titulo}
 🗓 *Data:* {data}
 🔗 *Link:* {link}
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
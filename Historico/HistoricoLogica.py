import tempfile

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from Globais.Globais import *


#Scraping
def obter_jogos():

    # Configurações do Chrome
    options = Options()
   # options.add_argument('--headless')

    # Inicializando o driver com o caminho do ChromeDriver e as opções
    driver = webdriver.Chrome(service=Service (ChromeDriverManager().install()), options=options)
    driver.get('https://tips.gg/pt/team/furia-csgo/')
    wait = WebDriverWait(driver, 10)

    # Espera até que a div principal com a classe 'answer' esteja presente
    div_principal = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'answer'))
    )

    # Espera até que a tabela dentro da div principal esteja presente
    tabela = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    ).find_element(By.TAG_NAME, 'tbody')

    jogos = []
    linhas = wait.until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )

    jogos = []
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, 'td')
        if len(colunas) >= 3:
            data = colunas[0].text.strip()
            adversario = colunas[1].text.strip()
            resultado = colunas[2].text.strip()
            jogos.append((data, adversario, resultado))
            if len(jogos) == 10:
                break

    return jogos



#FOrmatar dados extraidos dos ultimos jogos
def formatar_mensagem_jogos(jogos):
    mensagem = "📅 *Últimos Jogos da FURIA:*\n\n"
    for data, adversario, resultado in jogos:
        emoji = "🟢" if "Vitória" in resultado else "🔴"
        mensagem += f"*{data}* - 🆚 *{adversario}*\n"
        mensagem += f"{emoji} Resultado: *{resultado}*\n\n"
    return mensagem


def historico_jogos( message):
    nome = nome_usuario.get(message.from_user.id, 'Furioso(a)')
    bot.reply_to(message, f"Eaí {nome}! 🔥 Estamos buscando as últimas partidas da FURIA para você! 📅")
    try:
        jogos = obter_jogos()
        mensagem_resposta = formatar_mensagem_jogos(jogos)
    except Exception as erro:
        mensagem_resposta = "❌ Ocorreu um erro ao buscar os dados. Tente novamente mais tarde."
        print(f"[Erro Selenium] {erro}")

    bot.reply_to(message, mensagem_resposta, parse_mode='Markdown')
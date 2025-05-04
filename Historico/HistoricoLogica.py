import tempfile

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from Globais.Globais import *


#Scraping
def obter_jogos():
    # Cria um diretório temporário único para os dados do usuário
    temp_user_data_dir = tempfile.mkdtemp()

    # Configurações do Chrome
    options = Options()
    #options.add_argument('--headless')  # Executa sem abrir a janela
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/google-chrome'  # Caminho do Chrome/Chromium
    options.add_argument(f'--user-data-dir={temp_user_data_dir}')  # Diretório de dados do usuário

    # Caminho do chromedriver
    service = Service('/usr/local/bin/chromedriver')

    try:
        # Inicializando o driver com o caminho do ChromeDriver e as opções
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://tips.gg/pt/team/furia-csgo/')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div_principal = soup.find('div', class_='answer')
        tabela = div_principal.find('table').find('tbody')

        jogos = []
        for linha in tabela.find_all('tr'):
            colunas = linha.find_all('td')
            data = colunas[0].text.strip()
            adversario = colunas[1].text.strip()
            resultado = colunas[2].text.strip()
            jogos.append((data, adversario, resultado))

        return jogos
    finally:
        if 'driver' in locals() and driver:
            driver.quit()


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
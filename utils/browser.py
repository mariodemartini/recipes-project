from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    # Adiciona argumentos opcionais
    for option in options:
        chrome_options.add_argument(option)

    try:
        chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
        browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
        return browser
    except WebDriverException as e:
        print(f"Erro ao iniciar o navegador: {e}")
        return None

if __name__ == '__main__':
    # parâmetro '--headless' faz o navegador executar por baixo dos panos 
    browser = make_chrome_browser('--headless')

    if browser:
        try:
            browser.get('http://www.udemy.com/')
            # Use espera explícita ou implícita aqui, se necessário
            sleep(5)
        finally:
            browser.quit()

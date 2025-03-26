from selenium.webdriver.common.by import By
from bot import Bot

class DownloadDesativados:
    def __init__(self):
        """
            Inicializa o Webbot
        """
        try:
            self.bot = Bot.get_instance()
        except Exception as e:
            print(f"Erro ao inicializar o bot: {e}")
            raise
    
    def acessar_team(self):
        """
            Acessa a página de equipe tupperware.
        """
        try:
            self.bot.find_element("//h1[contains(., 'Home')]", By.XPATH, ensure_visible=True)  
            self.bot.browse("https://fv.tupperware.com.br/#!/team")
        except Exception as e:
            print(f"Erro ao acessar a página de equipe: {e}")
            raise
    
    def selecionar_situacao_comercial(self):
        """
            Seleciona a situação comercial dos membros da equipe.
        """
        try:
            self.bot.find_element("//md-select[contains(., 'Escolha a situação comercial')]", By.XPATH, ensure_clickable=True).click()
            self.bot.find_element("//md-option[contains(., 'Desativado')]", By.XPATH, ensure_clickable=True).click()
            self.bot.key_esc()
            self.bot.find_element("//button[contains(., 'Consultar')]", By.XPATH, ensure_clickable=True).click()
        except Exception as e:
            print(f"Erro ao selecionar a situação comercial: {e}")
            raise

    def baixar_arquivo(self):
        """
            Consulta os membros desativados e exporta para Excel.
        """
        self.bot.find_element("//button[contains(., 'Exportar para excel')]", By.XPATH, ensure_clickable=True).click()
        self.bot.find_element("//button[contains(., 'Ir para downloads')]", By.XPATH, ensure_clickable=True).click()
        self.bot.find_element("//span[contains(., 'Download pronto')]", By.XPATH, 20000, ensure_visible=True)
        self.bot.find_element("//button[contains(., 'Baixar')]", By.XPATH, ensure_clickable=True).click()

    def download(self):
        """
            Executa o bot.
        """
        try:
            self.acessar_team()
            self.selecionar_situacao_comercial()
            self.baixar_arquivo()
        finally:
            print("Processo de download finalizado.")
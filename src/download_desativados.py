from selenium.webdriver.common.by import By
from config_logging import logger
from bot import Bot

class DownloadDesativados:
    def __init__(self):
        """
            Inicializa o Webbot.
        """
        try:
            logger.info("Inicializando o bot.")
            self.bot = Bot.get_instance()
        except Exception as e:
            logger.error(f"Erro ao inicializar o bot: {e}")
            raise
        else:
            logger.success("Instância do bot inicializada com sucesso.")
    
    def acessar_team(self):
        """
            Acessa a página de equipe Tupperware.
        """
        try:
            logger.info("Acessando a página de equipe Tupperware.")
            self.bot.find_element("//h1[contains(., 'Home')]", By.XPATH, ensure_visible=True)  
            self.bot.browse("https://fv.tupperware.com.br/#!/team")
        except Exception as e:
            logger.error(f"Erro ao acessar a página de team Tupperware: {e}")
            raise
        else:
            logger.success("Página de equipe acessada com sucesso.")
    
    def selecionar_situacao_comercial(self):
        """
            Seleciona a situação comercial dos membros da equipe.
        """
        try:
            logger.info("Selecionando a situação comercial dos membros da equipe.")
            self.bot.find_element("//md-select[contains(., 'Escolha a situação comercial')]", By.XPATH, ensure_clickable=True).click()
            self.bot.find_element("//md-option[contains(., 'Desativado')]", By.XPATH, ensure_clickable=True).click()
            self.bot.key_esc()
            self.bot.find_element("//button[contains(., 'Consultar')]", By.XPATH, ensure_clickable=True).click()
        except Exception as e:
            logger.error(f"Erro ao selecionar a situação comercial: {e}")
            raise
        else:
            logger.success("Situação comercial selecionada com sucesso.")

    def baixar_arquivo(self):
        """
            Consulta os membros desativados e exporta para Excel.
        """
        try:
            logger.info("Consultando os membros desativados e exportando para Excel.")
            self.bot.find_element("//button[contains(., 'Exportar para excel')]", By.XPATH, ensure_clickable=True).click()
            self.bot.find_element("//button[contains(., 'Ir para downloads')]", By.XPATH, ensure_clickable=True).click()
            self.bot.find_element("//span[contains(., 'Download pronto')]", By.XPATH, 20000, ensure_visible=True)
            self.bot.find_element("//button[contains(., 'Baixar')]", By.XPATH, ensure_clickable=True).click()
        except Exception as e:
            logger.error(f"Erro ao baixar o arquivo: {e}")
            raise
        else:
            logger.success("Arquivo baixado com sucesso.")

    def download(self):
        """
            Executa o bot.
        """
        try:
            logger.info("➥ Inicializa o procedimento de Download.")
            self.acessar_team()
            self.selecionar_situacao_comercial()
            self.baixar_arquivo()
        except Exception as e:
            logger.error(f"Erro no processo de download: {e}")
        else:
            logger.success("Procedimento de Download concluído.")
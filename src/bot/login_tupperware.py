from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bot.manager import Manager
from config.logging import logger
import os

class LoginTupperware:
    def __init__(self, headless=False):
        """
            Inicializa o Webbot e 
            carrega as variáveis de ambiente
        """
        try:
            logger.info("Iniciando as credenciais de acesso.")
            load_dotenv()
            self.username = os.getenv("USERNAME")
            self.password = os.getenv("PASSWORD")
        except Exception as e:
            logger.error(f"Erro ao inicializar as credenciais de acesso: {e}")
        else:
            logger.success("Credenciais inicializadas com sucesso.")
        
        try:
            logger.info("Inicializando o bot.")
            self.bot = Manager.get_instance()
        except Exception as e:
            logger.error(f"Erro ao inicializar o bot: {e}")
            raise
        else:
            logger.success("Instância do bot inicializada com sucesso.")

    def acessar_site(self):
        """
            Abre o site da Tupperware
        """
        try:
            logger.info("Acessando o site da Tupperware...")
            self.bot.browse("https://fv.tupperware.com.br/#!/")
        except Exception as e:
            logger.error(f"Erro ao acessar o site: {e}")
            raise
        else:
            logger.success("Site da Tupperware acessado com sucesso.")
    
    def login(self):
        """
            Realiza o login no site da Tupperware
        """
        try:
            logger.info("➥ Inicializa o procedimento de Login.")
            self.acessar_site()

            inputs = {}
            labels = self.bot.find_elements("//label", By.XPATH, ensure_visible=True)
            
            for label in labels:
                text = label.text.strip().lower()
                if text == "login":
                    input_id = label.get_attribute("for")
                    if input_id:
                        inputs["login"] = self.bot.find_element(f"//input[@id='{input_id}']", By.XPATH)
                    else:
                        inputs["login"] = label.find_element("./following-sibling::input", By.XPATH)
                elif text == "senha":
                    input_id = label.get_attribute("for")
                    if input_id:
                        inputs["senha"] = self.bot.find_element(f"//input[@id='{input_id}']", By.XPATH)
                    else:
                        inputs["senha"] = label.find_element("./following-sibling::input", By.XPATH)
            if "login" in inputs and "senha" in inputs:
                logger.info(f"Preenchendo as credenciais de login.")
                inputs["login"].send_keys(self.username)
                inputs["senha"].send_keys(self.password)
            else:
                logger.error("Erro ao encontrar os campos de login e senha.")
                raise
            
            try:
                self.bot.find_element("//button[contains(text(), 'Entrar')]", By.XPATH).click()
            except Exception as e:
                logger.error(f"Erro ao clicar no botão de login: {e}")
                raise
            else:
                logger.success("Botão de login selecionado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao realizar o login: {e}")
            raise
        else:
            logger.success("Procedimento de Login concluído.")

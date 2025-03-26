import os
from bot import Bot
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

class LoginTupperware:
    def __init__(self, headless=False):
        """
            Inicializa o Webbot e 
            carrega as variáveis de ambiente
        """
        try:
            load_dotenv()

            self.username = os.getenv("USERNAME")
            self.password = os.getenv("PASSWORD")

            self.bot = Bot.get_instance()
        except Exception as e:
            print(f"Erro ao inicializar o bot: {e}")
            raise

    def acessar_site(self):
        """
            Abre o site da Tupperware
        """
        try:
            self.bot.browse("https://fv.tupperware.com.br/#!/")
        except Exception as e:
            print(f"Erro ao acessar o site: {e}")
            raise
    
    def login(self):
        """
            Realiza o login no site da Tupperware
        """
        try:
            self.acessar_site()

            inputs = {}
            labels = self.bot.find_elements("//label", By.XPATH, 20000)
            
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
                inputs["login"].send_keys(self.username)
                inputs["senha"].send_keys(self.password)
            else:
                raise Exception("Inputs não encontrados")
            
            try:
                self.bot.find_element("//button[contains(text(), 'Entrar')]", By.XPATH).click()
                
            except Exception as e:
                print(f"Erro ao clicar no botão de login: {e}")
                raise
        except Exception as e:
            print(f"Erro ao realizar o login: {e}")
            raise
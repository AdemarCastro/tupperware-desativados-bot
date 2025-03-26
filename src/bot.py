from botcity.web import WebBot
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Bot:
    _instance = None

    @staticmethod
    def get_instance():
        """
            Retorna a instância do bot.
            Caso não exista, cria uma nova.
        """
        if Bot._instance is None:
            Bot._instance = WebBot()
            Bot._instance.headless = False
            service = Service(ChromeDriverManager().install())
            Bot._instance.driver_path = service.path
        return Bot._instance
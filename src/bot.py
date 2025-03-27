from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from botcity.web.browsers.chrome import default_options
from botcity.web import WebBot
import os

class Bot:
    _instance = None

    @staticmethod
    def get_instance():
        """
            Retorna a instância do bot.
            Caso não exista, cria uma nova instância.
            Durante a criação, define o diretório de download.
        """
        if Bot._instance is None:
            Bot._instance = WebBot()
            Bot._instance.headless = False

            download_folder_path = os.path.join(os.getcwd(), "downloads")
            if not os.path.exists(download_folder_path):
                os.makedirs(download_folder_path)

            def_options = default_options(
                headless=Bot._instance.headless,
                download_folder_path=download_folder_path
            )

            service = Service(ChromeDriverManager().install())
            Bot._instance.driver_path = service.path            
            Bot._instance.options = def_options
        return Bot._instance
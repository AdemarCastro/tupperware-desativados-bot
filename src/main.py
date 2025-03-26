from botcity.web import WebBot
from botcity.maestro import BotMaestroSDK
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.headless = False

    service = Service(ChromeDriverManager().install())
    bot.driver_path = service.path

    bot.browse("https://fv.tupperware.com.br/#!/")

    input("Pressione Enter para finalizar...")
    bot.stop_browser()

if __name__ == "__main__":
    main()
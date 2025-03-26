from botcity.maestro import BotMaestroSDK
from login_tupperware import LoginTupperware
from download_desativados import DownloadDesativados
from bot import Bot

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = Bot.get_instance()

    LoginTupperware().login()

    DownloadDesativados().download()



    input("Pressione Enter para finalizar...")
    bot.stop_browser()

if __name__ == "__main__":
    main()
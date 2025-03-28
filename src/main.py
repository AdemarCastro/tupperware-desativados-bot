from botcity.maestro import BotMaestroSDK
from bot.login_tupperware import LoginTupperware
from bot.download_desativados import DownloadDesativados
from bot.manager import Manager
from utils.helpers import ler_arquivos, encontrar_interseccao, df_para_pdf

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = Manager.get_instance()

    LoginTupperware().login()

    DownloadDesativados().download()

    df_desativados, df_cadastrados = ler_arquivos()

    df = encontrar_interseccao(df_desativados, df_cadastrados)

    df_para_pdf(df)

    input("Pressione Enter para finalizar...")
    # bot.stop_browser()

if __name__ == "__main__":
    main()
from botcity.maestro import BotMaestroSDK
from bot.login_tupperware import LoginTupperware
from bot.download_desativados import DownloadDesativados
from bot.manager import Manager
from mail.mail_google import MailGoogle
from utils.helpers import ler_arquivos, encontrar_interseccao, df_para_pdf, fake_dataframe
import os

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = Manager.get_instance()

    LoginTupperware().login()

    DownloadDesativados().download()

    bot.wait(6000)

    df_desativados, df_cadastrados = ler_arquivos()

    df_interseccao = encontrar_interseccao(df_desativados, df_cadastrados)

    df_para_pdf(df_interseccao, nome_pdf="dataframe.pdf")

    mail = MailGoogle()

    NOME_DESTINATARIO = os.getenv("NOME_DESTINATARIO")
    EMAIL_DESTINATARIO = [os.getenv("EMAIL_DESTINATARIO")]
    ASSUNTO = os.getenv("ASSUNTO")

    CORPO_EMAIL = f"""
    <p>Olá <strong>{NOME_DESTINATARIO}</strong>,</p>

    <p>Segue em anexo o relatório de desativados para sua análise.<br/>
    Por favor, fique à vontade para me chamar caso tenha qualquer dúvida ou precise de mais informações.</p>

    <p>Agradeço pela atenção.</p>

    <p>Atenciosamente,<br/>
    Ademar Alves Castro Filho</p>
    """

    ANEXOS = [os.getenv("ANEXOS")]

    mail.enviar_email(EMAIL_DESTINATARIO, ASSUNTO, CORPO_EMAIL, ANEXOS)

    mail.desconectar()

    bot.stop_browser()

if __name__ == "__main__":
    main()
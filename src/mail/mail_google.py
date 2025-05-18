from botcity.plugins.email import BotEmailPlugin, MailServers
from config.logging import logger
import os

class MailGoogle:
    def __init__(self):
        """
        Configura as variáveis de acesso da sua conta Google.
        """
        try:
            logger.info("Inicializando o serviço de e-mail.")

            email_usuario = os.getenv("EMAIL_USUARIO")
            senha_usuario = os.getenv("SENHA_USUARIO")
            
            if not email_usuario or not senha_usuario:
                raise ValueError("Credenciais de e-mail não encontradas nas variáveis de ambiente")
                
            self.email = BotEmailPlugin.config_email(MailServers.GMAIL, email_usuario, senha_usuario)
        except Exception as e:
            logger.error(f"Erro ao inicializar o serviço de e-mail: {e}")
            raise
        else:
            logger.success(f"Serviço de e-mail inicializado com sucesso para: {email_usuario}")

    def enviar_email(self, destinatarios, assunto, corpo_email, anexos=None, use_html=True):
        """
        Envia um e-mail com os parâmetros fornecidos.

        :param destinatarios: Lista de e-mails dos destinatários.
        :param assunto: Assunto do e-mail.
        :param corpo_email: Corpo do e-mail (pode ser em HTML ou texto simples).
        :param anexos: Lista de caminhos de arquivos a serem enviados como anexo (opcional).
        :param use_html: Indica se o corpo do e-mail será enviado em HTML (padrão: True).
        """
        try:
            logger.info(f"Preparando envio de e-mail para {', '.join(destinatarios)}.")
            
            if anexos:
                logger.info(f"Anexando arquivos: {anexos}")
                
            self.email.send_message(assunto, corpo_email, destinatarios, attachments=anexos, use_html=use_html)
        except Exception as e:
            logger.error(f"Erro ao enviar o e-mail: {e}")
            raise
        else:
            logger.success(f"E-mail enviado com sucesso para {', '.join(destinatarios)}!")

    def desconectar(self):
        """
        Desconecta do servidor de e-mail.
        """
        try:
            logger.info("Desconectando do servidor de e-mail.")
            self.email.disconnect()
        except Exception as e:
            logger.error(f"Erro ao desconectar do servidor de e-mail: {e}")
            raise
        else:
            logger.success("Desconectado do servidor de e-mail com sucesso.")

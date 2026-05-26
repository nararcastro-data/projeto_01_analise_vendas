import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path


class EmailSender:
    def __init__(self):
        load_dotenv()
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_destinatario = os.getenv('EMAIL_DESTINATARIO')
        self._validar_credenciais()
    
    def _validar_credenciais(self):
        if not all([self.email_user, self.email_password, self.email_destinatario]):
            raise ValueError("Credenciais de email não configuradas no .env")
    
    def _validar_arquivo(self, caminho_arquivo):
        arquivo = Path(caminho_arquivo)
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        if not arquivo.is_file():
            raise ValueError(f"Caminho não é um arquivo: {caminho_arquivo}")
        return arquivo
    
    def _dataframe_para_html(self, df):
        return df.to_html(
            index=False,
            border=1,
            classes='table',
            justify='center'
        )
    
    def _criar_html_estilizado(self, titulo, conteudo_html):
        return f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h2 {{ color: #2c3e50; }}
                    .table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    .table th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; }}
                    .table td {{ padding: 10px; border: 1px solid #ddd; }}
                    .table tr:nth-child(even) {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h2>{titulo}</h2>
                {conteudo_html}
            </body>
        </html>
        """
    
    def enviar_relatorio(self, assunto, titulo, df=None, conteudo_texto="", anexos=[]):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.email_destinatario
            msg['Subject'] = assunto
            
            # Criar corpo HTML
            if df is not None:
                tabela_html = self._dataframe_para_html(df)
                corpo_html = self._criar_html_estilizado(titulo, tabela_html)
            else:
                corpo_html = self._criar_html_estilizado(titulo, f"<p>{conteudo_texto}</p>")
            
            msg.attach(MIMEText(corpo_html, 'html'))
            
            # Anexar arquivos
            for anexo in anexos:
                arquivo = self._validar_arquivo(anexo)
                with open(arquivo, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={arquivo.name}')
                    msg.attach(part)
            
            # Enviar email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            print(f"Email enviado com sucesso para {self.email_destinatario}")
            return True
            
        except FileNotFoundError as e:
            print(f"Erro: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar email: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    sender = EmailSender()
    
    # Exemplo com DataFrame
    df_exemplo = pd.DataFrame({
        'Produto': ['A', 'B', 'C'],
        'Vendas': [100, 200, 150]
    })
    
    sender.enviar_relatorio(
        assunto="Relatório de Vendas",
        titulo="Resumo de Vendas do Mês",
        df=df_exemplo,
        anexos=['grafico_vendas.png']
    )

import pandas as pd
import psycopg2
import mysql.connector
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from email_sender import EmailSender

load_dotenv()

conn = None
conn_mysql = None

try:
    # ==============================
    # CONEXÃO POSTGRESQL
    # ==============================
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DATABASE'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('POSTGRES_PORT')
        )
        print("✅ Conexão PostgreSQL estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar no PostgreSQL: {e}")
        raise

    # ==============================
    # CONEXÃO MYSQL
    # ==============================
    try:
        conn_mysql = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        print("✅ Conexão MySQL estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar no MySQL: {e}")
        raise

    # ==============================
    # QUERY MYSQL
    # ==============================
    query_mysql = """
    SELECT data_venda, valor_venda
    FROM datadt_curso_python.vendas
    """

    try:
        df_mysql = pd.read_sql(query_mysql, conn_mysql)
        df_mysql['ano'] = pd.to_datetime(df_mysql['data_venda']).dt.year
    except Exception as e:
        print(f"❌ Erro ao executar query MySQL: {e}")
        raise

    df_mysql_group = df_mysql.groupby('ano')['valor_venda'].sum().reset_index()
    df_mysql_group = df_mysql_group.rename(columns={'valor_venda': 'total_vendas'})
    df_mysql_group['empresa'] = 'Empresa 01'

    # ==============================
    # QUERY POSTGRESQL
    # ==============================
    query_pg = """
    SELECT 'Empresa 02' as empresa,
           date_part('Year', data_venda) as ano,
           sum(valor) as total_vendas
    FROM vendas.nota_fiscal
    GROUP BY date_part('Year', data_venda)
    """

    try:
        df_pg = pd.read_sql(query_pg, conn)
        df_pg['ano'] = df_pg['ano'].astype(int)
    except Exception as e:
        print(f"❌ Erro ao executar query PostgreSQL: {e}")
        raise

    # ==============================
    # PROCESSAMENTO
    # ==============================
    df_uniao = pd.concat([df_mysql_group, df_pg], ignore_index=True)

    df_pivot = df_uniao.pivot(index='ano', columns='empresa', values='total_vendas')

    # ==============================
    # GRÁFICO
    # ==============================
    try:
        df_pivot.plot(kind='bar', figsize=(10, 6), logy=True)

        plt.title('Vendas por Ano e Empresa (Escala Log10)')
        plt.xlabel('Ano')
        plt.ylabel('Total de Vendas (Log10)')
        plt.xticks(rotation=0)
        plt.legend(title='Empresa')
        plt.tight_layout()

        plt.savefig('grafico_vendas.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("✅ Gráfico salvo com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao gerar gráfico: {e}")
        raise

    # ==============================
    # ENVIO DE EMAIL
    # ==============================
    try:
        email_sender = EmailSender()

        sucesso = email_sender.enviar_relatorio(
            assunto='Relatório de Vendas',
            titulo='Análise de Vendas',
            df=df_uniao,
            anexos=['grafico_vendas.png']
        )

        if sucesso:
            print("✅ Email enviado com sucesso!")
        else:
            print("⚠️ Falha no envio do email.")

    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        raise

# ==============================
# FECHAR CONEXÕES
# ==============================
finally:
    if conn:
        conn.close()
        print("🔒 Conexão PostgreSQL encerrada.")

    if conn_mysql:
        conn_mysql.close()
        print("🔒 Conexão MySQL encerrada.")
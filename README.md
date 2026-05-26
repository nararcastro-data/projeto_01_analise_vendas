# 📊 Projeto 01 — Análise de Vendas

Pipeline Python que extrai dados de vendas de dois bancos de dados (MySQL e PostgreSQL), consolida as informações, gera gráficos comparativos e envia relatórios automatizados por e-mail.

---

## 🚀 Funcionalidades

- Conexão com **MySQL** e **PostgreSQL** via variáveis de ambiente
- Extração e agregação de dados de vendas por ano e empresa
- Geração de gráfico comparativo em escala logarítmica
- Envio automático de relatório HTML por e-mail com gráfico em anexo
- Análise exploratória via Jupyter Notebook

---

## 📁 Estrutura

```
projeto_01/
├── projeto01.py          # Script principal
├── email_sender.py       # Classe EmailSender
├── gerar_grafico.py      # Geração de gráfico auxiliar
├── imports.py            # Imports centralizados
├── analise.ipynb         # Notebook de análise exploratória
├── requirements.txt      # Dependências
├── .env.example          # Modelo de variáveis de ambiente
└── documentacao.html     # Documentação do projeto
```

---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto_01.git
cd projeto_01
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais.

> ⚠️ Para Gmail, use uma [senha de aplicativo](https://myaccount.google.com/apppasswords), não a senha da conta.

---

## ▶️ Execução

```bash
python projeto01.py
```

Para análise exploratória:

```bash
jupyter notebook analise.ipynb
```

---

## 🛠️ Tecnologias

| Biblioteca | Uso |
|---|---|
| `pandas` | Manipulação de dados |
| `psycopg2` | Conector PostgreSQL |
| `mysql-connector-python` | Conector MySQL |
| `matplotlib` | Geração de gráficos |
| `python-dotenv` | Variáveis de ambiente |

---

## 📄 Documentação

Abra o arquivo `documentacao.html` no navegador para a documentação completa do projeto.

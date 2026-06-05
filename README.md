# Livraria

E-commerce de livraria desenvolvido em **Python/Flask** com **MySQL**, como projeto da disciplina CMPLGP4 (Linguagem de Programação 4) — IFSP Campus Campinas.

## Funcionalidades

- Cadastro e login de usuários (sessão)
- Listagem de produtos na página inicial
- Carrinho de compras com controle de estoque
- Pagamento simulado com cartão de crédito
- Baixa automática no estoque após a compra
- Histórico de compras por usuário

## Tecnologias

- Python
- Flask
- MySQL
- HTML, CSS e JavaScript

## Estrutura do projeto

```
lp4/
├── app/
│   ├── __init__.py          # Factory da aplicação
│   ├── config.py            # Configurações
│   ├── database/            # Conexão com MySQL
│   ├── routes/              # Rotas (auth, carrinho, pagamento...)
│   ├── services/            # Regras de negócio
│   ├── templates/           # Páginas HTML
│   └── static/              # CSS e JS
├── database/
│   └── schema.sql           # Criação do banco e dados iniciais
├── run.py                   # Inicia o servidor
├── requirements.txt
└── .env.example
```

## Pré-requisitos

- Python 3.10+
- MySQL 8+
- pip

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Rafaela-Mello/livraria_simples.git
cd lp4
```

2. Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com seus dados do MySQL:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=livraria
SECRET_KEY=uma-chave-secreta-aleatoria
```

5. Crie o banco de dados:

```bash
mysql -u root -p < database/schema.sql
```

No Ubuntu, se o root usar autenticação por socket:

```bash
sudo mysql < database/schema.sql
```

## Executando

```bash
python run.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

## Observações

- O pagamento é **simulado** — nenhum dado real de cartão é processado.
- O arquivo `.env` não deve ser enviado ao GitHub (já está no `.gitignore`).
- O banco é criado com **12 livros** de exemplo prontos para teste.

## Autora

Rafaela Mello,
Projeto acadêmico — IFSP Campinas.

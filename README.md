# BD-2

Sistema que utiliza FastAPI para controle de estoque, cadastro de usuários e autenticação JWT, construída com FastAPI e SQLite.

## Funcionalidades

- Cadastro e autenticação de usuários (com JWT ou API Key)
- Controle de estoque: cadastro, atualização, consulta de itens
- Criação e consulta de pedidos (orders)
- Limitação de requisições por minuto em endpoints sensíveis
- Middleware de CORS configurado para integração com frontends modernos

## Principais tecnologias utilizadas

- **FastAPI** — Construção rápida e intuitiva de APIs RESTful
- **Starlette** — Middleware, CORS e toda base assíncrona
- **SQLAlchemy** — ORM para gerenciamento do banco
- **sqlite3** — Banco de dados local e leve
- **slowapi** — Limitação de requisições (rate-limit)
- **python-jose** — JWT para autenticação segura
- **Pydantic** — Validação e serialização de dados (embutido no FastAPI)
- **wrapt** — Utilitário para decorators (dependência da stack)

## Como rodar

1. **Instale as dependências** (no diretório do projeto):
    ```bash
    pip install fastapi sqlalchemy python-jose[cryptography] starlette slowapi pydantic wrapt
    ```

2. **Inicie o servidor**:
    ```bash
    uvicorn IntegrationApplication.integration_api.integration_application:app --reload
    ```
    - Altere o caminho acima conforme a estrutura do seu projeto.

## Organização dos principais arquivos

- `integration_application.py` — Criação do app, middlewares e routers
- `db.py` & `database.py` — Inicialização e configuração do banco (SQLite e SQLAlchemy)
- `routes.py` — Endpoints da API
- `security_manager.py` — Autenticação via JWT/API Key
- `item_model.py` — Manipulação de estoque e pedidos

## Observação
- O banco de dados padrão é local (`sqlite`), mas pode ser facilmente adaptado para PostgreSQL, MySQL, etc.

---

Sinta-se livre para adaptar o readme conforme seu público e a evolução do projeto! Caso queira um exemplo completo de uso dos endpoints ou doc com Swagger, posso detalhar também.
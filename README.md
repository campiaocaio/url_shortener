
![status](https://img.shields.io/badge/status-EM%20DESENVOLVIMENTO-yellow)

# URL Shortener API

> ⚠️ **Este projeto está em desenvolvimento ativo. Funcionalidades, endpoints e estrutura podem mudar a qualquer momento.**

Uma API FastAPI simples e robusta para encurtar URLs com contador de acessos.

## 🚀 Características

- ✅ **Criar URLs encurtadas** com slugs customizados
- ✅ **Redirecionar** para URL original via slug
- ✅ **Contador de acessos** (hits) por URL
- ✅ **Validação de slugs duplicados** com tratamento de erro HTTP 400
- ✅ **Testes unitários** (CRUD) e integração (HTTP)
- ✅ **Banco de dados PostgreSQL** com SQLAlchemy ORM
- ✅ **Documentação automática** Swagger UI

## 📋 Pré-requisitos

- **Python 3.9+**
- **PostgreSQL 12+**
- **pip** ou **conda**

## 🔧 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/url_shortener.git
cd url_shortener
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais PostgreSQL:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=shortener_db
DB_HOST=localhost
DB_PORT=5432
```

### 5. Criar banco de dados (se não existir)

```bash
psql -U postgres
CREATE DATABASE shortener_db;
CREATE USER shortener_user WITH PASSWORD 'futebol';
GRANT ALL PRIVILEGES ON DATABASE shortener_db TO shortener_user;
```

## 🚀 Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000**

Documentação Swagger: **http://127.0.0.1:8000/docs**

## 📝 Uso da API

### Criar URL encurtada

```bash
curl -X POST "http://127.0.0.1:8000/create" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "github",
    "target_url": "https://github.com"
  }'
```

**Resposta (HTTP 200):**
```json
{
  "target_url": "https://github.com",
  "id": 1,
  "slug": "github",
  "created_at": "2025-11-15T02:00:00.000000",
  "hits": 0
}
```

### Acessar URL encurtada

```bash
curl -X GET "http://127.0.0.1:8000/github"
```

**Resposta (HTTP 200):**
```json
{
  "target_url": "https://github.com"
}
```

*Nota: Cada acesso incrementa o contador `hits` no banco de dados.*

### Tentar criar slug duplicado

```bash
curl -X POST "http://127.0.0.1:8000/create" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "github",
    "target_url": "https://other-url.com"
  }'
```

**Resposta (HTTP 400):**
```json
{
  "detail": "Slug já existe"
}
```

## 🧪 Testes

### Testes Unitários (CRUD)

Testa as funções Python isoladamente usando SQLite em memória:

```bash
python -m pytest tests/test_crud.py -v
```

**Resultado esperado:** 4 testes passando

### Testes de Integração (API HTTP)

Testa os endpoints HTTP contra o servidor rodando:

1. **Terminal 1**: Inicie o servidor
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Terminal 2**: Execute os testes
   ```bash
   python tests/test_api.py
   ```

**Resultado esperado:** Todos os testes passando

## 📁 Estrutura do Projeto

```
url_shortener/
├── app/
│   ├── __init__.py           # Package initializer
│   ├── main.py               # Rotas FastAPI
│   ├── database.py           # Configuração SQLAlchemy
│   ├── models.py             # Modelos ORM (SQL)
│   ├── schemas.py            # Schemas Pydantic (validação)
│   └── crud.py               # Funções CRUD com tratamento de erro
│
├── tests/
│   ├── __init__.py
│   ├── test_crud.py          # Testes unitários (pytest)
│   └── test_api.py           # Testes de integração (requests)
│
├── requirements.txt          # Dependências Python
├── .env.example              # Template de variáveis de ambiente
├── .gitignore                # Arquivos a ignorar no Git
├── LICENSE                   # Licença MIT
└── README.md                 # Este arquivo
```

## 🏗️ Arquitetura

### Fluxo de dados

```
Cliente HTTP
    ↓
FastAPI Router (/create, /{slug})
    ↓
Dependência (get_db) - SessionLocal
    ↓
Funções CRUD (app/crud.py)
    ↓
Models ORM (app/models.py)
    ↓
SQLAlchemy Engine
    ↓
PostgreSQL Database
```

### Tratamento de erros

| Operação | Erro | Status HTTP | Mensagem |
|----------|------|-----------|----------|
| POST /create com slug duplicado | IntegrityError | 400 | "Slug já existe" |
| GET /{slug} não encontrado | QueryError | 404 | "Slug não encontrado" |
| Outros erros | Exception | 500 | Detalhes do erro |

## 🔐 Segurança

- ✅ Variáveis de ambiente para credenciais (não hardcoded)
- ✅ Validação de entrada com Pydantic
- ✅ Constraint único no banco para slugs
- ✅ Tratamento de exceções SQL (IntegrityError)

## 📦 Dependências principais

- **FastAPI 0.111.1** - Framework web assíncrono
- **Uvicorn 0.30.1** - Servidor ASGI
- **SQLAlchemy 2.0.31** - ORM Python
- **Psycopg2 2.9.9** - Driver PostgreSQL
- **Pydantic 2.x** - Validação de dados
- **Pytest 7.4.3** - Framework de testes
- **Requests 2.31.0** - Cliente HTTP para testes

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Autor:** Seu Nome
- **Email:** seu.email@exemplo.com
- **GitHub:** [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- FastAPI por ser um framework fantástico
- SQLAlchemy pela excelente abstração de banco de dados
- PostgreSQL pela robustez e confiabilidade

---

**Desenvolvido com ❤️ em Python**

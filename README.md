# 🧩 URL Shortener – Python API + Infraestrutura Completa

Este projeto é um URL Shortener desenvolvido em Python (FastAPI) com persistência de dados em PostgreSQL, estruturado como um estudo completo de infraestrutura, automação e boas práticas de arquitetura.

O foco do projeto vai além da API: ele cobre todo o ciclo de criação de um ambiente profissional, desde o provisionamento de máquinas virtuais até segurança, monitoramento e automação.

---

## 🚀 Tecnologias e Conceitos Utilizados

### 🖥️ Infraestrutura

- Virtualização utilizando VirtualBox
- Sistema Operacional alvo: Rocky Linux
- Tipos de rede: NAT, Bridge, Redes Internas
- Roteamento e comunicação entre VMs

### 🌐 Serviços

- Nginx como proxy reverso
- PostgreSQL (versão 18 prevista) como banco de dados
- Prometheus + Node Exporter para métricas (scraping)
- Grafana (opcional) para dashboards

### 🔐 Segurança

- firewalld configurado com política padrão DROP
- Abertura seletiva apenas das portas necessárias (SSH, API, DB, monitoramento)
- Usuários e credenciais isoladas para serviços

### 🤖 Automação

- Ansible para provisionamento e gerenciamento das VMs
- Playbooks para instalação, hardening e configuração de firewall
- Deploy básico da aplicação via tasks/handlers do Ansible

---

## 🧪 Aplicação – URL Shortener

- Implementada com FastAPI
- Banco de dados PostgreSQL com tabela `urls`
- Funcionalidades principais:
  - Criar URLs encurtadas (com slug customizável)
  - Resolver/Redirecionar para a URL original
  - Registrar acessos (`hits`) por URL
- Boas práticas adotadas:
  - Validação com Pydantic
  - Tratamento de erros de integridade (slug duplicado → HTTP 400)
  - Variáveis de ambiente para credenciais e configuração
- Para documentação completa da API, veja [`app/README_API.md`](app/README_API.md)

---

## 🎯 Objetivo do Projeto

Este projeto simula um ambiente real de produção para fins de estudo e aprendizado em DevOps/engenharia de infraestrutura. Os objetivos incluem:

- Criar uma API funcional e testável
- Construir a infraestrutura necessária para rodar a aplicação
- Integrar automação, segurança e monitoramento
- Documentar e exemplificar práticas operacionais (backup, hardening, observabilidade)

---

## 📚 Estrutura (resumo)

```
url_shortener/
├── app/
│   ├── __init__.py           # Package initializer
│   ├── main.py               # Rotas FastAPI
│   ├── database.py           # Configuração SQLAlchemy
│   ├── models.py             # Modelos ORM (SQL)
│   ├── schemas.py            # Schemas Pydantic (validação)
│   ├── crud.py               # Funções CRUD com tratamento de erro
│   └── README_API.md         # Documentação da API
│
├── tests/
│   ├── __init__.py
│   ├── test_crud.py          # Testes unitários (pytest)
│   └── test_api.py           # Testes de integração (requests)
│
├── Ansible/
│   └── firewall-seguro.yml   # Playbook de configuração de firewall
│
├── requirements.txt          # Dependências Python
├── .env.example              # Template de variáveis de ambiente
├── .gitignore                # Arquivos a ignorar no Git
├── LICENSE                   # Licença MIT
└── README.md                 # Este arquivo (visão geral do projeto)
```

---

## ✅ Próximos passos

- Incluir 9100/tcp (node_exporter) no playbook `Ansible/firewall-seguro.yml` para permitir scraping do Prometheus
- Criar playbooks separados por funções (db, api, monitoring) e usar roles para reuso

---

Desenvolvido como um projeto educacional e referência para práticas de infraestrutura e devops aplicada a uma aplicação Python.

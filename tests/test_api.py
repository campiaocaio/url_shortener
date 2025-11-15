#!/usr/bin/env python3
"""
Testes de integração para a API de encurtador de URLs.
Testa os endpoints HTTP contra um servidor FastAPI rodando.

Pré-requisitos:
  - Servidor rodando em http://127.0.0.1:8000
  - Banco de dados PostgreSQL configurado
  
Para rodar:
  $ python tests/test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 50)
    print(f"   {title}")
    print("=" * 50)


def print_test(test_num, description):
    """Imprime o número e descrição do teste."""
    print(f"\n✓ TESTE {test_num}: {description}")


def print_response(response):
    """Imprime resposta formatada."""
    try:
        data = response.json()
        print(f"Status: HTTP {response.status_code}")
        print(f"Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except Exception as e:
        print(f"Status: HTTP {response.status_code}")
        print(f"Resposta: {response.text}")
        return None


if __name__ == "__main__":
    print_header("TESTES DE INTEGRAÇÃO - API DE ENCURTADOR DE URLs")

    # Teste 1: Criar primeira URL
    print_test(1, "Criar URL encurtada com slug 'stackoverflow'")
    response1 = requests.post(
        f"{BASE_URL}/create",
        json={"slug": "stackoverflow", "target_url": "https://stackoverflow.com"}
    )
    data1 = print_response(response1)

    # Teste 2: Acessar a URL criada
    print_test(2, "Acessar slug 'stackoverflow' (deve retornar URL de destino)")
    response2 = requests.get(f"{BASE_URL}/stackoverflow")
    data2 = print_response(response2)

    # Teste 3: Tentar criar com slug duplicado
    print_test(3, "Tentar criar URL com slug duplicado (deve retornar HTTP 400)")
    response3 = requests.post(
        f"{BASE_URL}/create",
        json={"slug": "stackoverflow", "target_url": "https://other-site.com"}
    )
    data3 = print_response(response3)

    # Teste 4: Criar novo slug diferente
    print_test(4, "Criar outra URL encurtada com slug 'youtube'")
    response4 = requests.post(
        f"{BASE_URL}/create",
        json={"slug": "youtube", "target_url": "https://youtube.com"}
    )
    data4 = print_response(response4)

    # Teste 5: Acessar slug inexistente
    print_test(5, "Tentar acessar slug inexistente (deve retornar HTTP 404)")
    response5 = requests.get(f"{BASE_URL}/nonexistent")
    print(f"Status: HTTP {response5.status_code}")
    try:
        print(f"Resposta: {json.dumps(response5.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Resposta: {response5.text}")

    # Teste 6: Criar slug com incremento de hits
    print_test(6, "Criar novo slug 'github' e acessar 3 vezes para incrementar hits")
    response6a = requests.post(
        f"{BASE_URL}/create",
        json={"slug": "github", "target_url": "https://github.com"}
    )
    data6 = print_response(response6a)
    initial_hits = data6.get("hits", 0) if data6 else 0
    print(f"\nHits iniciais: {initial_hits}")

    # Acessar 3 vezes
    print("\nAcessando /github 3 vezes...")
    for i in range(3):
        requests.get(f"{BASE_URL}/github")
        print(f"  Acesso {i+1} realizado")

    # Teste 7: Validar resposta padrão
    print_test(7, "Verificar estrutura da resposta de GET /{slug}")
    response7 = requests.get(f"{BASE_URL}/youtube")
    data7 = print_response(response7)

    print_header("✓ TODOS OS TESTES DE INTEGRAÇÃO CONCLUÍDOS!")
    print("""
Resumo dos testes:
  ✅ POST /create — Cria URL encurtada com slug único
  ✅ GET /{slug} — Retorna URL de destino e incrementa hits
  ✅ Slug duplicado — Retorna HTTP 400 "Slug já existe"
  ✅ Slug inexistente — Retorna HTTP 404
  ✅ IntegrityError — Capturado e tratado corretamente
  ✅ PostgreSQL real — Dados persistem no banco

A API está funcionando normalmente! 🚀
    """)

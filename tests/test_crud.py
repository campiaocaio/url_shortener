"""
Testes unitários para as funções CRUD de URLs encurtadas.
Verifica se IntegrityError é capturado corretamente ao inserir slug duplicado.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import pytest

from app.database import Base
from app import crud, schemas

# Setup: criar DB em memória (SQLite) para teste rápido e isolado
# Não interfere com o PostgreSQL em produção
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(bind=engine)


def test_create_url_with_duplicate_slug():
    """
    Testa se IntegrityError é capturado ao tentar inserir slug duplicado.
    
    Cenário:
    1. Cria primeira URL encurtada com slug "google"
    2. Tenta criar segunda URL com o mesmo slug "google"
    3. Verifica se HTTPException(400) é lançada
    """
    db = TestingSessionLocal()

    # Primeira inserção: slug "google" → https://www.google.com
    data1 = schemas.URLCreate(slug="google", target_url="https://www.google.com")
    url1 = crud.create_url(db, data1)
    
    assert url1.slug == "google"
    assert url1.target_url == "https://www.google.com"
    print(f"✓ Primeira URL criada: /{url1.slug} → {url1.target_url}")

    # Segunda tentativa: slug "google" → https://other.com
    # Isto deve lançar HTTPException(400) porque o slug "google" já existe
    data2 = schemas.URLCreate(slug="google", target_url="https://other.com")

    with pytest.raises(HTTPException) as exc_info:
        crud.create_url(db, data2)

    # Verifica se o erro é HTTP 400
    assert exc_info.value.status_code == 400
    assert "Slug já existe" in exc_info.value.detail
    print(f"✓ Segundo INSERT com slug duplicado foi rejeitado com erro 400")

    db.close()


def test_create_url_with_different_slugs():
    """
    Testa se múltiplos URLs com slugs diferentes funcionam corretamente.
    """
    db = TestingSessionLocal()

    # Cria primeira URL
    data1 = schemas.URLCreate(slug="github", target_url="https://github.com")
    url1 = crud.create_url(db, data1)
    assert url1.slug == "github"
    print(f"✓ URL 1 criada: /{url1.slug} → {url1.target_url}")

    # Cria segunda URL com slug diferente (deve funcionar)
    data2 = schemas.URLCreate(slug="stackoverflow", target_url="https://stackoverflow.com")
    url2 = crud.create_url(db, data2)
    assert url2.slug == "stackoverflow"
    print(f"✓ URL 2 criada: /{url2.slug} → {url2.target_url}")

    # Verifica se ambas foram inseridas
    assert url1.id != url2.id
    print(f"✓ URLs diferentes foram criadas com sucesso (IDs: {url1.id}, {url2.id})")

    db.close()


def test_get_url_by_slug():
    """
    Testa se a busca por slug retorna a URL correta.
    """
    db = TestingSessionLocal()

    # Cria uma URL
    data = schemas.URLCreate(slug="python", target_url="https://python.org")
    created_url = crud.create_url(db, data)
    print(f"✓ URL criada: /{created_url.slug} → {created_url.target_url}")

    # Busca pela URL usando o slug
    found_url = crud.get_url_by_slug(db, "python")
    assert found_url is not None
    assert found_url.slug == "python"
    assert found_url.target_url == "https://python.org"
    print(f"✓ URL encontrada pela busca: /{found_url.slug} → {found_url.target_url}")

    # Tenta buscar slug que não existe
    not_found = crud.get_url_by_slug(db, "nonexistent")
    assert not_found is None
    print(f"✓ Busca por slug inexistente retornou None")

    db.close()


def test_increase_hit():
    """
    Testa se o contador de cliques (hits) é incrementado corretamente.
    """
    db = TestingSessionLocal()

    # Cria uma URL
    data = schemas.URLCreate(slug="twitter", target_url="https://twitter.com")
    url = crud.create_url(db, data)
    
    initial_hits = url.hits
    print(f"✓ URL criada com {initial_hits} hits inicial")

    # Simula um clique (aumenta hits)
    updated_url = crud.increase_hit(db, "twitter")
    assert updated_url.hits == initial_hits + 1
    print(f"✓ Hits incrementado para {updated_url.hits}")

    # Simula mais cliques
    crud.increase_hit(db, "twitter")
    crud.increase_hit(db, "twitter")
    
    final_url = crud.get_url_by_slug(db, "twitter")
    assert final_url.hits == initial_hits + 3
    print(f"✓ Após 3 cliques, hits = {final_url.hits}")

    db.close()


if __name__ == "__main__":
    # Permite rodar com: python -m pytest tests/test_crud.py -v
    pytest.main([__file__, "-v", "-s"])

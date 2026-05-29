import asyncio
import os
import httpx
from workout_api.main import app
from workout_api.configs.database import engine
from workout_api.contrib.models import BaseModel
import workout_api.atleta.models
import workout_api.categorias.models
import workout_api.centro_treinamento.models

async def run_tests():
    # Remove o banco de teste se já existir para começar do zero
    if os.path.exists("./workout.db"):
        os.remove("./workout.db")
        print("Banco de dados anterior removido.")

    # Garante a criação de tabelas diretamente
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    print("Tabelas criadas no banco de teste.")

    # Base URL fictícia para o ASGIApp
    base_url = "http://testserver"

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=base_url) as client:
        print("\n--- Iniciando os Testes de Integração ---\n")

        # 1. Teste de criação de Categoria
        print("Testando criação de categoria...")
        res_cat = await client.post("/categorias/", json={"nome": "Cardio"})
        assert res_cat.status_code == 201, f"Erro ao criar categoria: {res_cat.text}"
        print("Categoria 'Cardio' criada com sucesso!")

        # 2. Teste de Categoria Duplicada (IntegrityError -> 303)
        print("Testando criação de categoria duplicada...")
        res_cat_dup = await client.post("/categorias/", json={"nome": "Cardio"})
        assert res_cat_dup.status_code == 303, f"Status incorreto para categoria duplicada: {res_cat_dup.status_code}"
        assert "Já existe uma categoria cadastrada com o nome: Cardio" in res_cat_dup.json()["detail"], f"Mensagem incorreta: {res_cat_dup.text}"
        print("Tratamento de categoria duplicada OK (HTTP 303)!")

        # 3. Teste de criação de Centro de Treinamento
        print("Testando criação de centro de treinamento...")
        res_ct = await client.post("/centros_treinamento/", json={
            "nome": "CT Sparta",
            "endereco": "Rua das Flores, 123",
            "proprietario": "Leonidas"
        })
        assert res_ct.status_code == 201, f"Erro ao criar centro de treinamento: {res_ct.text}"
        print("Centro de treinamento 'CT Sparta' criado com sucesso!")

        # 4. Teste de Centro de Treinamento Duplicado (IntegrityError -> 303)
        print("Testando criação de CT duplicado...")
        res_ct_dup = await client.post("/centros_treinamento/", json={
            "nome": "CT Sparta",
            "endereco": "Rua das Flores, 123",
            "proprietario": "Leonidas"
        })
        assert res_ct_dup.status_code == 303, f"Status incorreto para CT duplicado: {res_ct_dup.status_code}"
        assert "Já existe um centro de treinamento cadastrado com o nome: CT Sparta" in res_ct_dup.json()["detail"], f"Mensagem incorreta: {res_ct_dup.text}"
        print("Tratamento de CT duplicado OK (HTTP 303)!")

        # 5. Teste de criação de Atleta
        print("Testando criação de atleta...")
        atleta_data = {
            "nome": "Gustavo",
            "cpf": "12345678900",
            "idade": 28,
            "peso": 80.5,
            "altura": 1.82,
            "sexo": "M",
            "categoria": {"nome": "Cardio"},
            "centro_treinamento": {"nome": "CT Sparta"}
        }
        res_atleta = await client.post("/atletas/", json=atleta_data)
        assert res_atleta.status_code == 201, f"Erro ao criar atleta: {res_atleta.text}"
        print("Atleta 'Gustavo' criado com sucesso!")

        # 6. Teste de Atleta Duplicado / CPF Duplicado (IntegrityError -> 303)
        print("Testando criação de atleta com CPF duplicado...")
        # Mesmos dados, principalmente mesmo CPF
        res_atleta_dup = await client.post("/atletas/", json=atleta_data)
        assert res_atleta_dup.status_code == 303, f"Status incorreto para atleta duplicado: {res_atleta_dup.status_code}"
        assert "Já existe um atleta cadastrado com o cpf: 12345678900" in res_atleta_dup.json()["detail"], f"Mensagem incorreta: {res_atleta_dup.text}"
        print("Tratamento de CPF duplicado OK (HTTP 303)!")

        # Cadastrar um segundo atleta para testar paginação e filtros
        print("Cadastrando segundo atleta para testes adicionais...")
        atleta_data_2 = {
            "nome": "Mariana",
            "cpf": "98765432100",
            "idade": 25,
            "peso": 60.0,
            "altura": 1.68,
            "sexo": "F",
            "categoria": {"nome": "Cardio"},
            "centro_treinamento": {"nome": "CT Sparta"}
        }
        await client.post("/atletas/", json=atleta_data_2)

        # 7. Teste de Listagem Customizada (GET /atletas/)
        print("Testando listagem customizada (response schema)...")
        res_list = await client.get("/atletas/")
        assert res_list.status_code == 200, f"Erro ao obter listagem: {res_list.text}"
        data = res_list.json()
        
        # O retorno do fastapi-pagination tem o formato: {"items": [...], "total": ..., "limit": ..., "offset": ...}
        assert "items" in data, "Estrutura de paginação ausente na listagem."
        assert len(data["items"]) == 2, f"Deveria ter 2 atletas cadastrados, tem {len(data['items'])}"
        
        item = data["items"][0]
        # Verificar se possui apenas nome, categoria e centro_treinamento
        assert "nome" in item, "Nome ausente"
        assert "categoria" in item, "Categoria ausente"
        assert "centro_treinamento" in item, "Centro de treinamento ausente"
        assert "cpf" not in item, "CPF deveria estar oculto na listagem"
        assert "idade" not in item, "Idade deveria estar oculta na listagem"
        assert "peso" not in item, "Peso deveria estar oculto na listagem"
        print("Listagem customizada OK (campos ocultados com sucesso)!")

        # 8. Teste de Paginação (limit e offset)
        print("Testando paginação (limit=1)...")
        res_page1 = await client.get("/atletas/?limit=1&offset=0")
        data_page1 = res_page1.json()
        assert len(data_page1["items"]) == 1, f"Deveria retornar 1 item, retornou {len(data_page1['items'])}"
        assert data_page1["total"] == 2, "O total geral de registros deveria ser 2"
        assert data_page1["limit"] == 1, "O limite retornado deveria ser 1"
        assert data_page1["offset"] == 0, "O offset retornado deveria ser 0"
        
        res_page2 = await client.get("/atletas/?limit=1&offset=1")
        data_page2 = res_page2.json()
        assert len(data_page2["items"]) == 1
        assert data_page2["items"][0]["nome"] != data_page1["items"][0]["nome"], "O segundo item deveria ser diferente do primeiro"
        print("Paginação Limit/Offset OK!")

        # 9. Teste de Filtros (nome e cpf)
        print("Testando filtro por nome (Mariana)...")
        res_filter_nome = await client.get("/atletas/?nome=Mariana")
        data_filter_nome = res_filter_nome.json()
        assert len(data_filter_nome["items"]) == 1, f"Deveria retornar 1 atleta com nome Mariana, retornou {len(data_filter_nome['items'])}"
        assert data_filter_nome["items"][0]["nome"] == "Mariana"

        print("Testando filtro por cpf (12345678900)...")
        res_filter_cpf = await client.get("/atletas/?cpf=12345678900")
        data_filter_cpf = res_filter_cpf.json()
        assert len(data_filter_cpf["items"]) == 1, f"Deveria retornar 1 atleta com o CPF informado, retornou {len(data_filter_cpf['items'])}"
        assert data_filter_cpf["items"][0]["nome"] == "Gustavo"

        print("Testando filtros não correspondentes...")
        res_filter_none = await client.get("/atletas/?nome=Inexistente")
        data_filter_none = res_filter_none.json()
        assert len(data_filter_none["items"]) == 0, "Deveria retornar uma lista vazia"
        print("Filtros via Query Parameters OK!")

        print("\n--- TODOS OS TESTES PASSARAM COM SUCESSO! ---\n")

if __name__ == "__main__":
    asyncio.run(run_tests())

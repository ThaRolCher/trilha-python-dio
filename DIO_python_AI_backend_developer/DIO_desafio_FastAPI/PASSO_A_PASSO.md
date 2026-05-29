# Guia Passo a Passo: Evoluindo a Workout API com Paginação, Filtros e Tratamento de Erros

Olá! Este guia foi preparado com muito carinho para conduzir você, passo a passo, no desenvolvimento do desafio da **Workout API** no Bootcamp da DIO. O objetivo é transformar a API base em uma aplicação muito mais robusta, profissional e pronta para cenários de produção.

Aqui aprenderemos a configurar paginação eficiente de dados, adicionar filtros flexíveis via Query Parameters, customizar payloads de resposta e tratar erros de integridade do banco de dados de maneira amigável, retornando respostas HTTP semânticas.

---

## Índice
1. [Conceitos Fundamentais](#1-conceitos-fundamentais)
2. [Configuração do Ambiente de Desenvolvimento](#2-configuração-do-ambiente-de-desenvolvimento)
3. [Configuração Simplificada do Banco de Dados (SQLite Assíncrono)](#3-configuração-simplificada-do-banco-de-dados-sqlite-assíncrono)
4. [Criação Automática das Tabelas (Lifespan do FastAPI)](#4-criação-automática-das-tabelas-lifespan-do-fastapi)
5. [Customização do Schema de Retorno do Atleta](#5-customização-do-schema-de-retorno-do-atleta)
6. [Paginação e Filtros no Endpoint de Atletas](#6-paginação-e-filtros-no-endpoint-de-atletas)
7. [Tratamento de Exceções de Integridade (HTTP 303)](#7-tratamento-de-exceções-de-integridade-http-303)
8. [Executando e Testando a API](#8-executando-e-testando-a-api)

---

## 1. Conceitos Fundamentais

Antes de colocarmos a mão na massa, vamos entender as tecnologias e conceitos que utilizaremos:

* **FastAPI:** Um framework web moderno, rápido (de alta performance) para construir APIs com Python, baseado em tipos padrão do Python (via Pydantic).
* **Pydantic:** Uma biblioteca de validação de dados e gerenciamento de configurações que garante que os dados de entrada e saída correspondam aos tipos declarados.
* **SQLAlchemy 2.0:** A biblioteca padrão de mapeamento objeto-relacional (ORM) do Python, permitindo interagir com o banco de dados usando classes Python em vez de SQL puro.
* **aiosqlite:** O driver que permite ao SQLAlchemy interagir de forma assíncrona com o SQLite.
* **fastapi-pagination:** Uma biblioteca que automatiza a paginação de resultados nas rotas do FastAPI, suportando nativamente paginações do tipo `Page` (página e tamanho) e `LimitOffsetPage` (limite e deslocamento).

---

## 2. Configuração do Ambiente de Desenvolvimento

Para garantir que nossas bibliotecas rodem sem conflitos, vamos criar um ambiente virtual (`venv`) e instalar as dependências necessárias.

### Passo 2.1: Criar o Ambiente Virtual
No terminal da raiz do seu projeto, execute o comando correspondente ao seu sistema operacional:

```bash
# Windows
python -m venv .venv

# Linux/macOS
python3 -m venv .venv
```

### Passo 2.2: Instalar as Dependências
Adicione as duas novas bibliotecas (`fastapi-pagination` e `aiosqlite`) no final do arquivo `requirements.txt`:

```text
fastapi-pagination==0.12.24
aiosqlite==0.20.0
```

E instale todas as dependências no seu ambiente virtual:

```bash
# Windows (PowerShell/CMD)
.\.venv\Scripts\pip install -r requirements.txt

# Linux/macOS
./.venv/bin/pip install -r requirements.txt
```

---

## 3. Configuração Simplificada do Banco de Dados (SQLite Assíncrono)

Por padrão, a Workout API é configurada para rodar com PostgreSQL. Para facilitar a execução local sem a obrigatoriedade de gerenciar contêineres Docker, nós configuramos uma URL de banco SQLite assíncrona como padrão no arquivo de configurações.

### Passo 3.1: Editar `workout_api/configs/settings.py`
Substitua a URL PostgreSQL pela URL do SQLite assíncrono:

```python
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Alterado para SQLite assíncrono local
    DB_URL: str = Field(default='sqlite+aiosqlite:///./workout.db')

settings = Settings()
```

### Passo 3.2: Ajustar a Classe Base no SQLAlchemy
O SQLite não tem suporte nativo ao tipo `PG_UUID` do dialeto do PostgreSQL. Para tornar nosso código compatível com múltiplos bancos de dados, ajustamos o identificador padrão (`id`) das tabelas em `workout_api/contrib/models.py` para usar o tipo genérico `UUID` do SQLAlchemy, que traduz o campo automaticamente para `VARCHAR(36)` no SQLite e para `UUID` no PostgreSQL:

```python
from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4, nullable=False)
```

---

## 4. Criação Automática das Tabelas (Lifespan do FastAPI)

Para facilitar a primeira execução, em vez de exigir que você execute comandos de migração complexos do Alembic, configuramos a criação das tabelas de forma automática toda vez que o servidor da aplicação inicia. 

Para isso, usamos o gerenciador de ciclo de vida (`lifespan`) do FastAPI.

### Passo 4.1: Editar `workout_api/main.py`
Atualize o arquivo para registrar o lifespan e os modelos do banco de dados:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routers import api_router
from workout_api.configs.database import engine
from workout_api.contrib.models import BaseModel

# Importamos os modelos para registrá-los na classe base do SQLAlchemy
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas do banco de dados se elas não existirem no startup
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield

app = FastAPI(title='WorkoutApi', lifespan=lifespan)
app.include_router(api_router)

# Registramos a paginação global na nossa aplicação FastAPI
add_pagination(app)
```

---

## 5. Customização do Schema de Retorno do Atleta

Para a rota de listagem geral de atletas, o desafio solicita uma resposta reduzida contendo apenas `nome`, `centro_treinamento` e `categoria`. 

### Passo 5.1: Criar o Schema `AtletaResponse` em `workout_api/atleta/schemas.py`
Adicione o seguinte schema abaixo da classe `AtletaOut`:

```python
class AtletaResponse(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]
```

Dessa forma, quando a API listar os atletas, ela ocultará campos desnecessários como CPF, peso, altura, data de criação e sexo, otimizando o payload de resposta.

---

## 6. Paginação e Filtros no Endpoint de Atletas

Agora, vamos atualizar a lógica de consulta no controller de atletas para receber filtros opcionais por query parameters (`nome` e `cpf`) e aplicar a paginação no banco de dados.

### Passo 6.1: Atualizar `workout_api/atleta/controller.py`
Modifique as importações e reescreva a rota `query` (`GET /atletas/`):

```python
from typing import Optional
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate

# ... outras importações ...

@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaResponse], # Retorna a estrutura paginada customizada
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = None, # Parâmetro opcional de busca
    cpf: Optional[str] = None,  # Parâmetro opcional de busca
) -> LimitOffsetPage[AtletaResponse]:
    
    # Criamos a query base de seleção de atletas
    query_stmt = select(AtletaModel)
    
    # Aplicamos os filtros dinamicamente com base nas query parameters fornecidas
    if nome:
        query_stmt = query_stmt.filter(AtletaModel.nome == nome)
    if cpf:
        query_stmt = query_stmt.filter(AtletaModel.cpf == cpf)
        
    # A função paginate executa a paginação de forma assíncrona no banco
    return await paginate(db_session, query_stmt)
```

---

## 7. Tratamento de Exceções de Integridade (HTTP 303)

Erros internos de restrições de banco (como CPFs duplicados ou nomes duplicados) geram um erro do tipo `IntegrityError` no SQLAlchemy. Caso esse erro não seja tratado, o FastAPI retornará um código genérico `500 Internal Server Error`. 

Para evitar isso, capturamos essa exceção de forma explícita e retornamos o status code `303 See Other` com uma mensagem amigável contendo o valor conflitante.

### Passo 7.1: Tratamento no Módulo de Atletas (`workout_api/atleta/controller.py`)
No endpoint `post`, adicione o bloco `try...except IntegrityError`:

```python
from sqlalchemy.exc import IntegrityError

@router.post(...)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    # ... busca de categoria e centro de treinamento ...
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        # Se ocorrer uma violação de chave única (CPF duplicado)
        raise HTTPException(
            status_code=303,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return atleta_out
```

### Passo 7.2: Tratamento nos Outros Módulos
Também adicionamos o mesmo padrão de tratamento nos endpoints de criação dos outros módulos para garantir integridade completa na API:

* **Categorias (`workout_api/categorias/controller.py`):**
  ```python
  except IntegrityError:
      raise HTTPException(
          status_code=303,
          detail=f'Já existe uma categoria cadastrada com o nome: {categoria_in.nome}'
      )
  ```

* **Centros de Treinamento (`workout_api/centro_treinamento/controller.py`):**
  ```python
  except IntegrityError:
      raise HTTPException(
          status_code=303,
          detail=f'Já existe um centro de treinamento cadastrado com o nome: {centro_treinamento_in.nome}'
      )
  ```

---

## 8. Executando e Testando a API

### Passo 8.1: Iniciar o Servidor
Execute o Uvicorn a partir do diretório raiz da sua aplicação:

```bash
# Certifique-se de que sua venv está ativada no seu terminal
uvicorn workout_api.main:app --reload
```

### Passo 8.2: Acessar a Documentação Interativa
Abra o navegador e acesse a URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Lá você encontrará a interface do Swagger UI, onde poderá testar todos os endpoints:
1. **Criar Categoria e Centro de Treinamento:** Envie requisições `POST /categorias/` e `POST /centros_treinamento/`.
2. **Criar um Atleta:** Crie um atleta associando os nomes da categoria e do centro de treinamento recém-criados.
3. **Testar CPF Duplicado:** Tente submeter o mesmo atleta novamente e verifique se o retorno é `303 See Other` com a mensagem `"Já existe um atleta cadastrado com o cpf: [CPF_ENVIADO]"`.
4. **Testar Listagem Customizada e Paginação:** Acesse `GET /atletas/` informando valores nos campos `limit` (ex: 2) e `offset` (ex: 0) para observar a paginação limit-offset e a estrutura de dados contendo apenas `nome`, `categoria` e `centro_treinamento`.
5. **Testar Filtros:** Informe os parâmetros `nome` ou `cpf` na URL do `GET /atletas/` para testar a filtragem de busca.

---

Bons estudos e muito sucesso nos seus projetos! Se precisar de ajuda, revise cada passo com atenção. 😎

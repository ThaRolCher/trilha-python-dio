from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routers import api_router
from workout_api.configs.database import engine
from workout_api.contrib.models import BaseModel

# Importar os modelos para que sejam registrados no BaseModel
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield

app = FastAPI(title='WorkoutApi', lifespan=lifespan)
app.include_router(api_router)
add_pagination(app)

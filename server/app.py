from fastapi import FastAPI

from api.router import router as main_router
from starlette.middleware.cors import CORSMiddleware
from settings.settings import settings

app = FastAPI()
app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

if settings.DEBUG:
    import uvicorn

    uvicorn.run(app)

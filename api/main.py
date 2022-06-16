from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.dependencies import get_version
from api.routes import examples, tasks

app = FastAPI(
    title="Demo API",
    docs_url="/api/docs",
    version=get_version(),
)

app.include_router(examples.router)
app.include_router(tasks.router)


@app.get("/", include_in_schema=False)
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse("/api/docs")

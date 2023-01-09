from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.dependencies import get_version
from api.routes import run, tasks

app = FastAPI(
    title="Demo API",
    docs_url="/api/docs",
    version=get_version(),
)

app.include_router(run.router)
app.include_router(tasks.router)


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
def redirect_to_docs() -> str:
    return "/api/docs"

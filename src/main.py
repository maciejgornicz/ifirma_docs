from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from modules.health import health
from modules.uploader import IFirmaUploader, DirectoryWatcher
from modules.settings import settings


app = FastAPI()

ifirma_uploader = IFirmaUploader(settings.ifirma.login, settings.ifirma.password)
directory_watcher = DirectoryWatcher(ifirma_uploader)


@app.get('/healthcheck')
def healthcheck() -> dict[str, str]:
    if health.alive:
        return {'message': 'alive'}
    else:
        raise HTTPException(503)

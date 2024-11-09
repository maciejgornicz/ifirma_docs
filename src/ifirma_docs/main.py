from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from ifirma_docs.modules import health
from ifirma_docs.models import IFirmaUploader, DirectoryWatcher
from ifirma_docs.modules.settings import settings

app = FastAPI()

ifirma_uploader = IFirmaUploader(settings.ifirma.login, settings.ifirma.password)
directory_watcher = DirectoryWatcher(ifirma_uploader)


@app.get('/healthcheck')
def healthcheck():
    if health.alive:
        return {'message': 'alive'}
    else:
        raise HTTPException(503)

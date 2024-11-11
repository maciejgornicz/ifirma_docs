# test_uploader.py
from modules.uploader import IFirmaUploader, DirectoryWatcher, health, settings
from time import sleep
import os
import pytest  # type: ignore


@pytest.fixture(autouse=True)
def initialize_and_clean():
    # settings.watched_dir = './data'
    yield
    if os.path.isfile(f'{settings.watched_dir}/tmp.file'):
        os.remove(f'{settings.watched_dir}/tmp.file')


@pytest.fixture()
def watcher():
    uploader = IFirmaUploader('test', 'test')
    watcher = DirectoryWatcher(uploader)

    return watcher


def test_hearbeat(mocker, watcher):
    mocker.patch('modules.uploader.health.heartbeat')
    sleep(watcher._check_interval+0.1)
    watcher.stop()
    health.heartbeat.assert_called()


def test_upload_and_delete_finded_file(mocker, watcher):
    mocker.patch('modules.uploader.IFirmaUploader._upload_file_to_ifirma')
    with open(os.path.join(settings.watched_dir, 'tmp.file'), 'w') as file:
        file.write("tests")
    sleep(watcher._check_interval+0.1)
    watcher.stop()
    watcher._ifirma_uploader._upload_file_to_ifirma.assert_called_once()
    assert not os.path.isfile(os.path.join(settings.watched_dir, 'tmp.file'))

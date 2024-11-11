from selenium import webdriver
from threading import Thread
import os
import time
from modules.health import health
from modules.settings import settings
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pydantic import SecretStr


class IFirmaUploader():
    """Class using browser to maintain IFirma connections"""
    def __init__(self, username: SecretStr, password: SecretStr) -> None:
        self._username = username
        self._password = password

        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument('--ignore-ssl-errors=yes')
        self._chrome_options.add_argument('--ignore-certificate-errors')

    def _upload_file_to_ifirma(self, file: str) -> None:
        """Uploads file to IFirma documents"""
        with webdriver.Remote(settings.webdriver.url,
                              options=self._chrome_options) as browser:
            browser.get(settings.ifirma.url)
            browser.find_element(By.ID,
                                 "login").send_keys(settings.ifirma.login.get_secret_value())
            browser.find_element(By.ID,
                                 "password").send_keys(settings.ifirma.password.get_secret_value())
            browser.maximize_window()

            browser.find_element(By.ID, "loginButton").click()
            time.sleep(10)
            # browser.execute_script("just_close();")
            try:
                browser.find_element(By.XPATH, "//button[contains(.,'Pomiń')]").click()
            except NoSuchElementException:
                pass

            browser.find_element(By.XPATH,
                                 "//span[contains(.,'E-Dokumenty')]/..").click()
            time.sleep(1)
            s = browser.find_element(By.XPATH, '//input[@type="file"]')
            s.send_keys(file)
            print(s)
            time.sleep(2)


class DirectoryWatcher():
    """Watcher class to watch file apear in directory"""
    def __init__(self, ifirma_uploader: IFirmaUploader,
                 check_interval: int = 1) -> None:
        self._directory = settings.watched_dir
        self._ifirma_uploader = ifirma_uploader
        self._check_interval = check_interval
        self._running = True
        self._watcher = Thread(target=self._watch)
        self._watcher.start()

    def _get_files(self) -> None:
        """Checks if file apear in directory and process it"""
        path = self._directory
        files = os.listdir(path)
        if files:
            for file in files:
                filepath = os.path.join(path, file)
                self._ifirma_uploader._upload_file_to_ifirma(file=filepath)
                os.remove(filepath)

    def _watch(self) -> None:
        """Main watcher loop"""
        while self._running:
            self._get_files()
            health.heartbeat()
            time.sleep(self._check_interval)

    def stop(self) -> None:
        self._running = False

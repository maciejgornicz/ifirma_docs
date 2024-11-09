from selenium import webdriver
from threading import Thread
import os
import time
from ifirma_docs.modules import settings, health
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support import expected_conditions as EC


class IFirmaUploader():
    def __init__(self, username, password) -> None:
        self._username = username
        self._password = password

        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument('--ignore-ssl-errors=yes')
        self._chrome_options.add_argument('--ignore-certificate-errors')

    def _upload_file_to_ifirma(self, file):
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
    def __init__(self, ifirma_uploader: IFirmaUploader,
                 check_interval: int = 1) -> None:
        self._directory = settings.watched_dir
        self._ifirma_uploader = ifirma_uploader
        self._check_interval = check_interval
        self._watcher = Thread(target=self._watch)
        self._watcher.start()

    def _get_files(self):
        files = os.listdir(self._directory)
        if files:
            for file in files:
                filepath = f"{self._directory}/{file}"
                self._ifirma_uploader._upload_file_to_ifirma(file=filepath)
                os.remove(filepath)

    def _watch(self):
        while True:
            self._get_files()
            health.heartbeat()
            time.sleep(self._check_interval)

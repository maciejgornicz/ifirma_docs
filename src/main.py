# Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

ifirma_url = "http://ifirma.pl/app"


def upload_file_to_ifirma(file):
    with webdriver.Remote("http://localhost:4444", options=options) as browser:

        # def login(driver , url, username, password):
        browser.get(ifirma_url)
        browser.find_element(By.ID, "login").send_keys("maciej.gornicz@havio.pl")
        browser.find_element(By.ID, "password").send_keys("Maciej2014fundacja")
        browser.maximize_window()

        browser.find_element(By.ID, "loginButton").click()
        time.sleep(0.5)
        browser.execute_script("just_close();")
        browser.find_element(By.XPATH, "//button[contains(.,'Pomiń')]").click()
        browser.find_element(By.XPATH, "//span[contains(.,'E-Dokumenty')]/..").click()
        time.sleep(1)
        s = browser.find_element(By.XPATH, '//input[@type="file"]')
        s.send_keys(file)
        print(s)
        time.sleep(15)


def process_directory():
    dirname = "./data"
    files = os.listdir(dirname)
    if files:
        for file in files:
            filepath = f"{dirname}/{file}"
            upload_file_to_ifirma(file=filepath)
            os.remove(filepath)
            print(filepath)


while True:
    process_directory()
    time.sleep(5)

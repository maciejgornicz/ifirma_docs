from selenium import webdriver

class IFirmaUploader():
    def __init__(self, username, password, watched_dir) -> None:
        self.username = username
        self.password = password

        self.watching_enabled = False
        self.watched_dir = watched_dir

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--ignore-ssl-errors=yes')
        self.chrome_options.add_argument('--ignore-certificate-errors')
    
    def upload_file_to_ifirma(file):
         with webdriver.Remote("http://localhost:4444", options=options) as browser:
        

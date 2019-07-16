from selenium import webdriver
import requests

class mini_crawler:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def search(self, keyword):
        url = "https://www.ecosia.org/images?q=%s" % keyword
        self.driver.get(url)

    def download(self):
        try:
            elements = self.driver.find_elements_by_class_name('image-result')
            links = set(map(lambda el: el.get_property('href'), elements))
        except Exception:
            pass
        else:
            paths = []
            for url in links:
                path = self.__download(url)
                if path:
                    paths.append(path)
            return paths

    def __download(self, url):
        try:
            response = requests.get(url)
        except Exception as e:
            return
        else:
            if response.status_code == 200:
                index = url.rfind('/')
                file = url[index + 1:]
                with open(file, 'wb') as f:
                    try:
                        f.write(response.content)
                    except Exception:
                        return
                return file

from selenium import webdriver
from os import path, makedirs
import requests
import time

class crawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    def stop(self):
        self.driver.stop()

    def search(self, keyword):
        """
            Open a headless browser directed to an ecosia search of the given keyword
            Adds the first shown pictures to the links set
        """
        self.keyword = keyword
        self.links = set()
        self.driver.get("https://www.ecosia.org/images?q=<%s>" % keyword)
        self.__update()

    def next(self):
        """
            Scrolls the browser to the bottom so ecosia loads more pictures
            Adds the new results to the links set
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the new images to appear, possibly change for a signal to be received when the html changes
        time.sleep(2)
        self.__update()

    def __update(self):
        """
            Updates the images set with all the results on the page
        """
        try:
            elements = self.driver.find_elements_by_class_name('image-result')
            for element in elements:
                self.links.add(element.get_property("href"))
        except:
            pass

    def next_links(self):
        """
            Returns the new results after scrolling to the bottom
        """
        old_links = self.links.copy()
        self.next()
        return self.links - old_links

    def download_one(self, url: str, folder='downloads'):
        self.directory = folder
        filename = path.join(folder, self.keyword, trim_url(url))
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)

    def download_many(self, urls, folder='downloads'):
        self.directory = folder
        create_directories(folder, self.keyword)
        directory_path = path.join(folder, self.keyword)
        for url in urls:
            filename = path.join(folder, self.keyword, trim_url(url))
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)

    def download_all(self, folder='downloads'):
        self.directory = folder
        create_directories(folder, self.keyword)
        directory_path = path.join(folder, self.keyword)
        for url in self.links:
            if not self.is_downloaded(url):
                filename = path.join(folder, self.keyword, trim_url(url))
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)

    def is_downloaded(self, url: str) -> bool:
        return path.exists(path.join(self.directory, self.keyword, trim_url(url)))

def create_directories(folder: str, sub_folder: str):
    try:
        if not path.exists(folder):
            makedirs(folder)
            time.sleep(0.2)
            if not path.exists(path.join(folder, sub_folder)):
                makedirs(sub_directory)
        else:
            sub_directory = path.join(folder, sub_folder)
            if not path.exists(sub_directory):
                makedirs(sub_directory)
    except Exception as e:
        print(e)

def trim_url(url: str):
    return url[url.rfind('/') + 1:]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from os import path, makedirs
import requests
import time

class crawler:
    def __init__(self, timeout=10):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.timeout = timeout
        self.session = requests.Session()

    def stop(self):
        self.driver.close()

    def search(self, keyword):
        """
            Open a headless browser directed to an ecosia search of the given keyword
            Adds the first shown pictures to the links set
        """
        self.keyword = keyword
        self.links = set()
        self.driver.get("https://www.ecosia.org/images?q=%s" % keyword)
        self.__update()

    def gather_more(self):
        """
            Scrolls the browser to the bottom so ecosia loads more pictures
            Adds the new results to the links set
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try: 
            # wait for loading element to appear
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.loading-animation")))
        except TimeoutException:
            raise ValueError("No more images found")

        try:    
            # then wait for the element to disappear from the viewport
            WebDriverWait(self.driver, self.timeout).until_not(lambda driver: driver.execute_script("\
                function elementInViewport(el) {\
                    let top = el.offsetTop;\
                    let left = el.offsetLeft;\
                    let width = el.offsetWidth;\
                    let height = el.offsetHeight;\
                    \
                    while(el.offsetParent) {\
                        el = el.offsetParent;\
                        top += el.offsetTop;\
                        left += el.offsetLeft;\
                    }\
                    \
                    return (\
                        top >= window.pageYOffset &&\
                        left >= window.pageXOffset &&\
                        (top + height) <= (window.pageYOffset + window.innerHeight) &&\
                        (left + width) <= (window.pageXOffset + window.innerWidth)\
                    );\
                }\
                let el = document.getElementsByClassName('loading-animation');\
                return elementInViewport(el)\
            "))
        except TimeoutException:
            raise ValueError("Lost internet connection")

        self.__update()

    def __update(self):
        """
            Updates the images set with all the results on the page
        """
        try:
            elements = self.driver.find_elements_by_class_name('image-result')
            self.links |= set(map(lambda element: element.get_property("href"), elements))
        except Exception as e:
            raise ValueError("Search did not return images")

    def next_links(self):
        """
            Returns the new results after scrolling to the bottom
        """
        old_links = self.links.copy()
        self.gather_more()
        return self.links - old_links

    def __download(self, url: str):
        """
            Downloads the image from the given url and saves it in a designated folder
        """
        filename = path.join(self.directory, self.keyword, trim_url(url))
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
        except Exception as e:
            return
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename

    def __download_one(self, url: str, folder='downloads'):
        self.directory = folder
        create_directories(self.directory, self.keyword)
        return self.__download(url)

    def __download_many(self, urls, folder='downloads'):
        self.directory = folder
        create_directories(self.directory, self.keyword)
        paths = []
        for url in urls:
            paths.append(self.__download(url))
        return paths

    def download_all(self, folder='downloads'):
        """
            Downloads all the gathered images links
            Checks every url so as to not download already saved images
        """
        self.directory = folder
        return self.__download_many(filter(lambda url: not self.is_downloaded(url), self.links), folder=self.directory)

    def download(self, n, folder='downloads', scroll=True):
        """
            Downloads a given number of images from the gathered links
            Checks every url so as to not download already saved images
            If it has no more usable links it will gather more
        """
        self.directory = folder
        filtered_links = list(filter(lambda url: not self.is_downloaded(url), self.links))
        if scroll and len(filtered_links) < n:
            while len(filtered_links) < n:
                new_links = self.next_links()
                filtered_links += filter(lambda url: not self.is_downloaded(url), new_links)
        return self.__download_many(filtered_links[:n])

    def is_downloaded(self, url: str) -> bool:
        """
            Checks to see if the 'would-be' assigned path already exists
        """
        return path.exists(path.join(self.directory, self.keyword, trim_url(url)))

def create_directories(folder: str, sub_folder: str):
    """
        Creates a folder and subfolder in the cwd if necessary
    """
    try:
        if not path.exists(folder):
            makedirs(folder)
            time.sleep(0.2)
            sub_directory = path.join(folder, sub_folder)
            if not path.exists(sub_directory):
                makedirs(sub_directory)
        else:
            sub_directory = path.join(folder, sub_folder)
            if not path.exists(sub_directory):
                makedirs(sub_directory)
    except Exception as e:
        print(e)

def trim_url(url: str):
    """
        Inclusively trims everything before the last / character
    """
    return url[url.rfind('/') + 1:]
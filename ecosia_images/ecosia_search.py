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

    def gather_more(self):
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
            self.links |= set(map(lambda element: element.get_property("href"), elements))
        except Exception as e:
            print(e)

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
        response = requests.get(url, stream=True)
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
                if len(new_links) == 0:
                    raise ValueError("No more images found")
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
            if not path.exists(path.join(folder, sub_folder)):
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
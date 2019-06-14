from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import requests
import time

size_options = [
    'small',
    'medium',
    'large',
    'wallpaper'
]

color_options = [
    'colorOnly',
    'monochrome',
    'red',
    'orange',
    'yellow',
    'green',
    'teal',
    'blue',
    'purple',
    'pink',
    'brown',
    'black',
    'gray'
]

type_options = [
    'photo',
    'clipart',
    'line',
    'animated'
]

freshness_options = [
    'day',
    'week',
    'month'
]

license_options = [
    'share',
    'shareCommercially',
    'modify',
    'modifyCommercially',
    'public'
]

download_options = {
    'size': size_options,
    'color': color_options,
    'image_type': type_options,
    'freshness': freshness_options,
    'license': license_options,
}


class crawler:

    def __init__(self, timeout=10, browser='chrome'):
        if browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        elif browser == 'firefox':
            firefox_options = webdriver.firefox.options.Options()
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--headless')
            self.driver = webdriver.Firefox(options=firefox_options)
        else:
            raise ValueError('Invalid browser option')
        self.timeout = timeout
        self.session = requests.Session()

    def stop(self):
        self.driver.quit()

    def search(self, keyword, **kwargs):
        """
            Open a headless browser and directs it
            to an ecosia search of the given keyword
            with the given options
        """
        options = {
            'size': '',
            'color': '',
            'image_type': '',
            'freshness': '',
            'license': '',
        }
        options.update(kwargs)
        validate_options(**options)

        strings = (
            keyword,
            options.pop('size'),
            options.pop('color'),
            options.pop('image_type'),
            options.pop('freshness'),
            options.pop('license')
        )

        self.keyword = keyword
        self.links = set()
        ecosia_url = "https://www.ecosia.org/images"
        query = "?q=%s&size=%s&color=%s&imageType=%s&freshness=%s&license=%s"
        self.driver.get(ecosia_url + query % strings)
        self.__update()

    def gather_more(self):
        """
            Scrolls the browser to the bottom so ecosia loads more pictures
            Adds the new results to the links set
        """
        try:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        except ConnectionRefusedError:
            raise TimeoutError("Lost internet connection")
        try:
            # wait for loading element to appear
            css_selector = (By.CSS_SELECTOR, "div.loading-animation")
            wait = WebDriverWait(self.driver, self.timeout)
            wait.until(EC.presence_of_element_located(css_selector))
        except TimeoutException:
            raise TimeoutError("No more images found")

        try:
            # then wait for the element to disappear from the viewport
            wait.until_not(element_in_viewport)
        except TimeoutException:
            raise TimeoutError("Lost internet connection")

        self.__update()

    def __update(self):
        """
            Updates the images set with all the results on the page
        """
        try:
            elements = self.driver.find_elements_by_class_name('image-result')
            self.links |= set(map(extract_href, elements))
        except Exception as e:
            raise TimeoutError("Search did not return images")
        finally:
            if not len(elements):
                raise TimeoutError("No more images found")

    def next_links(self):
        """
            Returns the new results after scrolling to the bottom
        """
        old_links = self.links.copy()
        self.gather_more()
        return self.links - old_links

    def __download(self, url: str):
        """
            Downloads the image from the given url
            and saves it in a designated folder
        """
        filename = os.path.join(self.directory, self.keyword, trim_url(url))
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError('Unable to connect to Internet')
        except Exception as e:
            raise TimeoutError('Connection took to long to download file')
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                try:
                    f.write(response.content)
                except requests.exceptions.ConnectionError: 
                    try:
                        os.remove(filename)
                    except FileNotFoundError:
                        pass
                    finally:
                        raise TimeoutError('Connection took long to download file')
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
            path = self.__download(url)
            if path:
                paths.append(path)
        return paths

    def download_all(self, folder='downloads'):
        """
            Downloads all the gathered images links
            Checks every url so as to not download already saved images
        """
        self.directory = folder
        return self.__download_many(filter(self.is_not_downloaded, self.links),
                                    folder=self.directory)

    def download(self, n, folder='downloads', scroll=True):
        """
            Downloads a given number of images from the gathered links
            Checks every url so as to not download already saved images
            If it has no more usable links it will gather more
        """
        self.directory = folder
        filtered_links = list(filter(self.is_not_downloaded, self.links))
        if scroll and len(filtered_links) < n:
            while len(filtered_links) < n:
                new_links = self.next_links()
                filtered_links += filter(self.is_not_downloaded, new_links)
        return self.__download_many(filtered_links[:n])

    def is_downloaded(self, url: str) -> bool:
        """
            Checks to see if the 'would-be' assigned path already exists
        """
        image_path = os.path.join(self.directory, self.keyword, trim_url(url))
        return os.path.exists(image_path)

    def is_not_downloaded(self, url: str) -> bool:
        return not self.is_downloaded(url)


def create_directories(folder: str, sub_folder: str):
    """
        Creates a folder and subfolder in the cwd if necessary
    """
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            time.sleep(0.2)
            sub_directory = os.path.join(folder, sub_folder)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
        else:
            sub_directory = os.path.join(folder, sub_folder)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
    except Exception as e:
        print(e)


def element_in_viewport(driver):
    driver.execute_script("\
        let el = document.getElementsByClassName('loading-animation');\
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
    ")


def trim_url(url: str):
    """
        Inclusively trims everything before the last / character
    """
    return url[url.rfind('/') + 1:]


def extract_href(element):
    return element.get_property("href")


def validate_options(**kwargs) -> bool:
    size = kwargs.pop('size')
    if size and size not in size_options:
        raise TimeoutError('Invalid size option, try with %s'
                         % str(size_options))
    color = kwargs.pop('color')
    if color and color not in color_options:
        raise TimeoutError('Invalid color option, try with %s'
                         % str(color_options))
    image_type = kwargs.pop('image_type')
    if image_type and image_type not in type_options:
        raise TimeoutError('Invalid type option, try with %s'
                         % str(type_options))
    freshness = kwargs.pop('freshness')
    if freshness and freshness not in freshness_options:
        raise TimeoutError('Invalid freshness option, try with %s'
                         % str(freshness_options))
    license = kwargs.pop('license')
    if license and license not in license_options:
        raise TimeoutError('Invalid license option, try with %s'
                         % str(license_options))

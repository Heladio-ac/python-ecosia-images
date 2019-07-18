from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import requests
import time
import hashlib

size_options = [
    'small',
    'medium',
    'large',
    'wallpaper',
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
    'gray',
]

type_options = [
    'photo',
    'clipart',
    'line',
    'animated',
]

freshness_options = [
    'day',
    'week',
    'month',
]

license_options = [
    'share',
    'shareCommercially',
    'modify',
    'modifyCommercially',
    'public',
]

download_options = {
    'size': size_options,
    'color': color_options,
    'image_type': type_options,
    'freshness': freshness_options,
    'license': license_options,
}

browser_options = [
    'chrome',
    'firefox',
]

naming_options = [
    'trim',
    'hash',
    'custom',
]


class crawler:

    def __init__(self, timeout=10, browser='chrome', directory='downloads',
                 makedirs=True, naming='trim', naming_function=None):
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
            raise ValueError('Invalid browser option, try with %s'
                             % str(browser_options))

        if naming not in naming_options:
            raise ValueError('Incorrect naming mode option, try with %s'
                             % str(naming_options))

        self.naming = naming
        self.naming_function = naming_function
        self.directory = directory
        self.makedirs = makedirs
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
            options.pop('license'),
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
            raise TimeoutError("No more images found")
        finally:
            if not len(elements):
                raise TimeoutError("Search did not return images")

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
        filename = self.generate_filename(url)
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
        except Exception as e:
            print('Connection took to long to download file')
            return
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                try:
                    f.write(response.content)
                except Exception:
                    try:
                        os.remove(filename)
                    except FileNotFoundError:
                        pass
                    finally:
                        print('Connection took to long to download file')
                        return
            return filename

    def __download_one(self, url: str):
        create_directories(self.directory, self.keyword)
        return self.__download(url)

    def __download_many(self, urls):
        create_directories(self.directory, self.keyword)
        paths = []
        for url in urls:
            path = self.__download(url)
            if path:
                paths.append(path)
        return paths

    def download_all(self):
        """
            Downloads all the gathered images links
            Checks every url so as to not download already saved images
        """
        filtered_links = filter(self.is_not_downloaded, self.links)
        return self.__download_many(filtered_links)

    def download(self, n, scroll=True):
        """
            Downloads a given number of images from the gathered links
            Checks every url so as to not download already saved images
            If it has no more usable links it will gather more
        """
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
        image_path = self.generate_filename(url)
        return os.path.exists(image_path)

    def is_not_downloaded(self, url: str) -> bool:
        return not self.is_downloaded(url)

    def generate_filename(self, url: str) -> str:
        if self.naming_function:
            return self.naming_function(url, self.directory, self.keyword)
        file = trim_url(url)
        if self.naming == 'hash':
            extension = os.path.splitext(file)[1]
            if '?' in extension:
                index = extension.find('?')
                extension = extension[:index]
            filename = os.path.join(
                self.directory, self.keyword, hashingURL(url))
            filename += extension
        elif self.naming == 'trim':
            filename = os.path.join(
                self.directory, self.keyword, file)
        return filename


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
    index = url.rfind('/')
    return url[index + 1:]


def hashingURL(url: str):
    md5_obj = hashlib.md5(url.encode('utf-8'))
    md5_obj.update(url.encode('utf-8'))
    return md5_obj.hexdigest()


def extract_href(element):
    return element.get_property("href")


def validate_options(**kwargs) -> bool:
    size = kwargs.pop('size')
    if size and size not in size_options:
        raise ValueError('Invalid size option, try with %s'
                         % str(size_options))
    color = kwargs.pop('color')
    if color and color not in color_options:
        raise ValueError('Invalid color option, try with %s'
                         % str(color_options))
    image_type = kwargs.pop('image_type')
    if image_type and image_type not in type_options:
        raise ValueError('Invalid type option, try with %s'
                         % str(type_options))
    freshness = kwargs.pop('freshness')
    if freshness and freshness not in freshness_options:
        raise ValueError('Invalid freshness option, try with %s'
                         % str(freshness_options))
    license = kwargs.pop('license')
    if license and license not in license_options:
        raise ValueError('Invalid license option, try with %s'
                         % str(license_options))

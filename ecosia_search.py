from selenium import webdriver
import time

class searcher:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

    def search(self, keywords):
        """
            Open a headless browser directed to an ecosia search of the given keywords
            Adds the first shown pictures to the links set
        """
        self.links = set()
        self.driver.get("https://www.ecosia.org/images?q=<%s>" % keywords)
        self.gather_links()

    def next(self):
        """
            Scrolls the browser to the bottom so ecosia loads more pictures
            Adds the new results to the links set
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the new images to appear, possibly change for a signal to be received when the html changes
        time.sleep(2)
        self.gather_links()

    def gather_links(self):
        """
            Updates the images set with all the results on the page
        """
        try:
            elements = self.driver.find_elements_by_class_name('image-result')
            for element in elements:
                self.links.add(element.get_property("href"))
        except:
            pass

    def gather_new_links(self):
        """
            Returns the new results after scrolling to the bottom
        """
        old_links = self.links.copy()
        self.next()
        return self.links - old_links
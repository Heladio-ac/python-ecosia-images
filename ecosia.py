from selenium import webdriver
import requests

class searcher:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
    
        self.driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)


    def search(self, keywords):
        self.driver.get("https://www.ecosia.org/images?q=<%s>" % keywords)
        try:
            elements = self.driver.find_elements_by_class_name('image-result')
            for element in elements:
                print(element.get_property("href"))
        except:
            print('Was not able to find an element with that name.')

x = searcher()
x.search('perritos')
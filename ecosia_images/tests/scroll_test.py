from ecosia_images import crawler
from ecosia_images import options

"""
    Test the scroll functionality
"""

print('Instantiating crawler')
searcher = crawler()
print('Searching')
searcher.search('testing')
print('Downloading')
try:
    searcher.download(60)
except ValueError as e:
    print(e)
else:
    print('Success')
finally:
    searcher.stop()

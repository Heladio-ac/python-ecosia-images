from ecosia_images import crawler

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
except ValueError:
    print('Did not found the loading animation')
else:
    print('Success')
finally:
    searcher.stop()
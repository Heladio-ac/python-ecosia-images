from ecosia_images import crawler

"""
    Test the downloads functionality
"""

def skip_previous_downloads():
    """
        Test if the script is capable of scrolling past previously downloaded images
        until it finds new images
    """
    print('Instantiating crawler')
    searcher = crawler()
    print('Searching')
    searcher.search('testing')
    print('Downloading')
    searcher.download(50)
    print('Stopping')
    searcher.stop()
    
    print('Instantiating crawler')
    searcher = crawler()
    print('Searching')
    searcher.search('testing')
    if len(searcher.download(5)) == 5:
        print('Success')
    searcher.stop()

skip_previous_downloads()
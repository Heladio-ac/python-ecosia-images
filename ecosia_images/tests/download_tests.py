from ecosia_images import crawler

"""
    Test the downloads functionality
"""

def skip_previous_downloads():
    """
        Test if the script is capable of scrolling past previously downloaded images
        until it finds new images
    """
    searcher = crawler()
    searcher.search('testing')
    searcher.download(50)
    searcher.stop()
    
    searcher = crawler()
    searcher.search('testing')
    assert len(searcher.download(5)) == 5
    searcher.stop()

skip_previous_downloads()
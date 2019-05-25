from ..ecosia_search import options
from ecosia_images import crawler

"""
    Test the downloads functionality
"""


def skip_previous_downloads():
    """
        Test if the script is capable of
        scrolling past previously downloaded images
        until it finds new images
    """
    print('Instantiating crawler')
    searcher = crawler()
    try:
        print('Searching')
        searcher.search('testing')
        print('Downloading')
        searcher.download(50)
    except Exception as e:
        print(e)
    finally:
        print('Stopping')
        searcher.stop()

    print('Instantiating crawler')
    searcher = crawler()
    print('Searching')
    searcher.search('testing')
    try:
        if len(searcher.download(5)) == 5:
            print('Success')
    except Exception as e:
        print(e)
    finally:
        searcher.stop()


def download_with_options():
    """
        Test if the script is able to download images
        with specified characteristics
    """
    print('Instantiating crawler')
    searcher = crawler()
    try:
        print('Searching')
        for key in options:
            for option in options[key]:
                print('Searching: ', key, option)
                searcher.search('testing', **{key: option})
                print(searcher.links)
        print('Success')
    except Exception as e:
        print(e.args[0])
    finally:
        print('Stopping')
        searcher.stop()


skip_previous_downloads()
download_with_options()

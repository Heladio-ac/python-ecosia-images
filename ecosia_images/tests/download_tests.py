from ecosia_images import download_options
from ecosia_images import crawler

"""
    Test the downloads functionality

    .. note:: usage::
    
             time python ecosia_images/tests/download_tests.py 
            This test, for 10 images, usually lasts 50 seconds
                (50 files, 2m4s; 100 files, 8m54s).
            c1: Creating first crawler...
            c1: Searching...
            c1: Downloading...
            c1: Stopping...
            c2: Creating second crawler...
            c2: Searching...
            c2: Expected new images: 50
            c2: Downloaded new images: 89
            c2: Success. More downloaded files than expected
            c2: Stopping...
            Instantiating crawler
            Searching
            name 'options' is not defined
            Stopping
            
            [With failing download_with_options()]
            [10 images] real	0m50.238s
            [50 images] real	1m54.717s
            [50 images] real	2m3.085s
            [100 images] real	8m52.944s
"""


def skip_previous_downloads(phrase, n_file=10, success_rate=0.1):
    """
        Test if the script is capable of
        scrolling past previously downloaded images
        until it finds new images.
        
        :param phrase: e.g. 'red cart', 'blue button', 'green login'.
        :param n_file: Quantity of images.
        :param success_rate: Default 0.1 (10%). 
            Between 0.0 and 1.0, not validated.
            If n_file= and downloads it will print 'Success'

        .. note:: out::
        
            c1: Creating first crawler...
            c1: Searching...
            c1: Downloading...
            [MAY] Connection took to long to download file, aborting            
            c1: Downloaded images: 9
            c1: Stopping...
            c2: Creating second crawler...
            c2: Searching...
            c2: Expected new images: 5
            c2: Downloaded new images: 8
            c2: Success. More downloaded files than expected
            c2: Stopping...                        

            [10 images] real	0m41.191s
            [10 images] real	0m48.253s
        
        .. note:: path::

            ├── downloads
            │   ├── button
            │   │   ├── 1024px-RedButton_LeftArrow.svg.png
            │   │   ├── 1415914174402575245.png
            │   │   └── vector-wood-media-player-button.jpg
            │   ├── cart
            │   │   ├── 1200px-Golfcart.JPG
            │   │   ├── CART_0123-Editweb-size.jpg
            │   │   └── Shopping-Cart1_banner.jpg
            ├── ecosia_images
            │   ├── ecosia_search.py
            │   └── tests
            │       ├── download_tests.py               
    """
    print('c1: Creating first crawler...')
    searcher = crawler()
    try:
        print('c1: Searching...')
        searcher.search(phrase)
        print('c1: Downloading...')
        n_down_c1 = len(searcher.download(n_file))
        print('c1: Downloaded images:', n_down_c1)
        searcher.download(n_file)
    except Exception as e:
        print(e)
    finally:
        print('c1: Stopping...')
        searcher.stop()

    succ_min = int(success_rate * n_file)
    print('c2: Creating second crawler...')
    searcher = crawler()
    print('c2: Searching...')
    searcher.search(phrase)
    print('c2: Expected new images:', succ_min)
    try:
        # e.g. on second attempt
        n_down_c2 = len(searcher.download(n_file))
        print('c2: Downloaded new images:', n_down_c2)
        if n_down_c2 >= succ_min:
            print('c2: Success. More downloaded files than expected')
        print('Download1; NonRepeated2; NR2/D1(High=best); SuccessMinLim')
        prop = (n_down_c2 / n_down_c1) if n_down_c1 else None  # avoid div by 0
        print('{0}; {1}; {2:.3g}; {3}'.format(n_down_c1, n_down_c2, prop, succ_min))
    except Exception as e:
        print(e)
    finally:
        print('c2: Stopping...')
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

print('This test, for 10 images, usually lasts 50 seconds')
print('    (50 files, 2m4s; 100 files, 8m54s).')
skip_previous_downloads(phrase='button', n_file=10, success_rate=0.5)
#download_with_options(size='small', color='red')

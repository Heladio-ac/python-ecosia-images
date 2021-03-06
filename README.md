# python-ecosia-images

Python module for searching and downloading images from Ecosia

## Installing

~~~
pip install ecosia-images
~~~

## Setup

The only requisite to work with the library is to have a web browser and its driver installed. Currently the package works with either Google Chrome or Firefox.

If using Google Chrome it is required to also have Chromedriver installed and reachable in PATH. See the [following link](https://sites.google.com/a/chromium.org/chromedriver/) for more information.

As for Firefox, Geckodriver is required to be installed and reachable in PATH.

## Examples

#### Start a crawler

~~~ python
>>> from ecosia_images import crawler
>>> searcher = crawler()
~~~

The browser to be used can be passed to the crawler constructor

~~~ python
>>> from ecosia_images import crawler
>>> searcher = crawler(browser='firefox')
~~~

To see all valid browser options, see `ecosia_images.browser_options`.

~~~ python
>>> from ecosia_images import browser_options
>>> browser_options
['chrome', 'firefox']
~~~

#### Search images and get the links to the pictures

After declaring a crawler and using it to search for a keyword, the resulting links will be accesible by the `links` property

~~~ python
>>> searcher = crawler()
>>> searcher.search('number 9')
>>> searcher.links
{ ... } # urls
~~~

#### Search with options

Searches can also include the options that Ecosia provides for refining results. The available keys and values for refining searches are stored in `ecosia_images.download_options`.

~~~ Python
>>> from ecosia_images import download_options
>>> download_options
{
    'size': ['small', 'medium', 'large', 'wallpaper'],
    'color': ['colorOnly', 'monochrome', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'brown', 'black', 'gray'],
    'image_type': ['photo', 'clipart', 'line', 'animated'],
    'freshness': ['day', 'week', 'month'],
    'license': ['share', 'shareCommercially', 'modify', 'modifyCommercially', 'public']
}
~~~

The selected options can be specified when calling the `search` method of the crawler.

~~~ Python
>>> searcher.search('trees', color='monochrome', size='wallpaper')
>>> searcher.links
{ ... } # links to big pictures of trees in black and white
~~~

#### Gather more links

If more links are needed the function `gather_more` can be used.

~~~ python
>>> searcher.search('bees')
>>> len(searcher.links)
50  # Give or take
>>> searcher.gather_more()
>>> len(searcher.links)
100 # Give or take
~~~

#### Download images

In all the following cases, the script first checks whether the image has been already downloaded so it does not download it again. The functions will return the file paths to the downloaded images.

The `download` function will download a given number of pictures and save them in a folder whose name coincides with the keyword. This folder will be created inside the one specified when calling the constructor. In the following example, the images would be saved inside __/path/to/folder/keyword/__.

~~~ python
>>> searcher = crawler(directory='/path/to/folder/')
>>> searcher.search('keyword')
>>> searcher.download(100)
[ ... ] # list with file paths
~~~

If no folder is specified, the images will be saved inside a new folder named __downloads__ located in the current working directory.

There is also the `download_all` function which will download all the currently available links in the crawler object

~~~ python
>>> searcher.search('pidgeons')
>>> searcher.download_all()
[ ... ]
~~~

#### Stoping the client

It is necessary to stop the crawler to avoid the leak of resources.

~~~ python
>>> searcher.stop()
~~~

#### Filenames

The naming convention to be used for the downloaded files can be passed to the crawler constructor. To see all valid naming options, see `ecosia_images.naming_options`.

~~~ python
>>> from ecosia_images import crawler, naming_options
>>> searcher = crawler(naming='hash')
>>> naming_options
['trim', 'hash']
~~~

##### Custom naming

For a specific naming convention, a function can be passed to the constructor. If you are planning to rename the files, make sure to use this functionality as renaming the files will interfere with the crawler's ability to avoid downloading duplicates.

The function must take three parameters: url, directory and keyword.

If you plan on not using the default folders provided by the library, disallow this option so no directories are created by the crawler.

~~~ python
>>> def custom_naming(url, directory, keyword):
...     # Function implementation
...     return filename
>>> searcher = crawler(naming_function=custom_naming, makedirs=False)
~~~

## Disclaimer

The dowloaded images come from the Ecosia search engine and they may have copyrights. Do not download or use any image that violates its copyright terms. You can take advantage of the `license` option of the `search` function to avoid using copyrighted material.

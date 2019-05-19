# python-ecosia-images

Python module for searching and downloading images from Ecosia

## Installing

~~~
pip install ecosia-images
~~~

## Examples

#### Search images and get the links to the pictures

After declaring a crawler and using it to search for a keyword, the resulting links will be accesible by the `links` property

~~~ python
>>> from ecosia_images import crawler
>>> searcher = crawler()
>>> searcher.search('number 9')
>>> searcher.links
{ ... }
~~~

#### Gather more links

If more links are needed the function `gather_more` can be used.

~~~ python
>>> searcher.search('bees')
>>> len(searcher.links)
50  # Give or take
>>> searcher.gather_more()
100 # Give or take
~~~

#### Download images

In all the following cases, the script first checks whether the image has been already downloaded so it does not downloads it again.

The `download` function will download a given number of pictures and save them in a folder whose name coincides with the keyword. This folder will be created inside the one specified when calling the function. In the following example, the images would be saved inside __/path/to/folder/keyword/__.

~~~ python
>>> searcher.search('keyword')
>>> searcher.download(100, '/path/to/folder/')
~~~

If no folder is specified, the images will be saved inside a new folder named __downloads__ located in the current working directory.

~~~ python
>>> searcher.search('apples')
>>> searcher.download(100)  # The pictures will be saved at ./downloads/apples/
~~~

There is also the `download_all` function which will download all the currently available links in the crawler object

~~~ python
>>> searcher.search('pidgeons')
>>> searcher.download_all()
~~~

#### Stoping the client

It is necessary to stop the crawler to avoid resource leak.

~~~ python
>>> searcher.stop()
~~~

## Disclaimer

The images come from the Ecosia search engine. They may have copyrights and the original creators own these. Do not download or use any image that violates its copyright terms.

import requests

def download(url: str, folder='./'):
    filename = folder + url[url.rfind('/') + 1:]
    response = requests.get(url, stream=True)
    if response.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(response.content)
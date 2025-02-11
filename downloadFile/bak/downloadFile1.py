#usr/bin/env python3
import requests

def download(url):
    getResponse = requests.get(url)
    fileName = url.split("/")[-1]
    with open(fileName, "wb") as outFile:
        outFile.write(getResponse.content)

download("https://en.wikipedia.org/static/images/icons/wikipedia.png")
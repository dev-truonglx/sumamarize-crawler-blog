import re
from typing import Optional
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel
import os
import codecs
import time
import cloudscraper

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Item(BaseModel):
    url: str


@app.post("/play-movie/")
async def read_item(item: Item):
    url = item.url
    print(item.url)
    # session = requests.session()
    # session.headers = 'content-type'
    # session.mount("http://", cfscrape.CloudflareScraper())
    # scraper = cfscrape.create_scraper(sess=session)
    # req = scraper.get(url).content

    # start = time.time()
    # f_name = str(start)+'result.html'
    # f = open(f_name, 'wb')
    # f.write(req)
    # f.close
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })  # returns a CloudScraper instance
    soup = scraper.get(url).content
    print(soup)

    pattern = re.compile(
        r'src=(["\'])(.*?)\1', re.MULTILINE | re.DOTALL)

    # soup = codecs.open(os.getcwd()+'/'+f_name, "r", "utf-8").read()
    # print(soup)

    soup = BeautifulSoup(soup, "html.parser")

    get_script = soup.find('script', text=pattern)
    conten_script = get_script.string

    url = re.findall(
        '\<source src=\"http[^\"]*"', conten_script)
    print(url)
    url_final = ''
    if len(url):
        url_final = re.findall('http[^\"]*', url[0])[0]

    print(url_final)
    return {"url": url_final}

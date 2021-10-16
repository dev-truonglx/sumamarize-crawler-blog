from typing import Optional

from fastapi import FastAPI
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import re
from pydantic import BaseModel
import cfscrape
import os
from selenium import webdriver

# from recaptcha import *

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
    session = requests.session()
    session.headers = 'content-type'
    session.mount("http://", cfscrape.CloudflareScraper())
    scraper = cfscrape.create_scraper(sess=session)
    req = scraper.get(url).content
    test = "truonglx"
    # print(test.encode('utf-8'))

    # Save request as HTML named as 'Result.html'
    f_name = 'Result.html'
    f = open(f_name, 'wb')
    f.write(req)
    f.close

    # Excute JavaScript file
    # start = time()
    # Optional argument, if not specified will search path.
    # print(os.getcwd())
    # driver = webdriver.Chrome(os.getcwd()+"/chromedriver")
    # driver.get(os.getcwd()+f_name)
    # print driver.page_source

    pattern = re.compile(
        r'src=(["\'])(.*?)\1', re.MULTILINE | re.DOTALL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    # news = requests.get(url, headers)
    # print(news)
    soup = BeautifulSoup(req, "html.parser")
    # soup = BeautifulSoup(driver.page_source, "lxml")
    print(soup)
    # title = soup.find(
    #     "a", {"class": ["fs-16 flex flex-hozi-center color-yellow border-style-1"]}).text
    # tap = soup.find(
    #     "div", {"class": ["fs-17 fw-700 padding-0-20 color-gray inline-flex height-40 flex-hozi-center bg-black border-l-t"]}).text
    get_script = soup.find('script', text=pattern)
    conten_script = get_script.string

    url = re.findall(
        '\<source src=\"http[^\"]*"', conten_script)
    print(url)
    url_final = ''
    if len(url):
        url_final = re.findall('http[^\"]*', url[0])[0]

    # return url_final
    print(url_final)
    return {"url": url_final}

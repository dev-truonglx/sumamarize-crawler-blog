
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import requests
import json


def crawNewsData(baseUrl, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('h3', class_='title-news')
    links = [link.find('a').attrs["href"] for link in titles]
    data = []
    for link in links:
        print(link)
        news = requests.get(baseUrl + link)
        soup = BeautifulSoup(news.content, "html.parser")
        if not soup.find("h1", {"class": "article-title"}):
            continue

        abstract = soup.find("h2", {'class': 'sapo'}).text
        title = soup.find("h1", {"class": "article-title"}).text

        body = soup.find("div", id="main-detail-body")
        content = ""
        check = len(list(body.findChildren("p", recursive=False)))
        try:
            for i in range(check):
                content += body.findChildren("p", recursive=False)[
                    i].text
        except:
            content = ""

        if not body.find("img"):
            continue

        image = body.find("img").attrs["src"]

        data.append({
            "title": title,
            "abstract": abstract,
            "content": content,
            "image": image,
        })
        print("======POST========")
        requests.post("http://13.214.56.12/api/create-post", {
            "title": title,
            "content": content,
            "image": image,
            "link": link,
            "baseUrl": baseUrl
        })
    return data


def writeToImage(image, text, position, font, color, maxLine):
    charPerLine = 650 // font.getsize('x')[0]
    pen = ImageDraw.Draw(image)
    yStart = position[1]
    xStart = position[0]
    point = 0
    prePoint = 0
    while point < len(text):
        prePoint = point
        point += charPerLine
        while point < len(text) and text[point] != " ":
            point -= 1
        pen.text((xStart, yStart),
                 text[prePoint:point], font=font, fill=color)
        yStart += font.getsize('hg')[1]
        maxLine -= 1
        if (maxLine == 0):
            if (point < len(text)):
                pen.text((xStart, yStart), "...", font=font, fill="black")
            break


def makeFastNews(data):
    for index, item in enumerate(data):
        # make new image and tool to draw
        image = Image.new('RGB', (650, 750), color="white")
        pen = ImageDraw.Draw(image)
        # load image from internet => resize => paste to main image
        pen.rectangle(((0, 0), (650, 300)), fill="grey")
        newsImage = Image.open(requests.get(item["image"], stream=True).raw)
        newsImage.thumbnail((650, 300), Image.ANTIALIAS)
        image.paste(newsImage, (650 // 2 - newsImage.width //
                    2, 300 // 2 - newsImage.height//2))
        # write title
        titleFont = ImageFont.truetype("font/arial.ttf", 22)
        writeToImage(image, item["title"], (10, 310), titleFont, "black", 3)
        abstractFont = ImageFont.truetype("font/arial.ttf", 15)
        writeToImage(image, item["abstract"],
                     (10, 390), abstractFont, "gray", 4)
        contentFont = ImageFont.truetype("font/arial.ttf", 20)
        writeToImage(image, item["content"],
                     (10, 460), contentFont, "black", 11)
        name = "news-" + str(index) + ".png"
        image.save("news/" + name)
        print("saved to " + "news/" + name)


def crawCafeF(baseUrl, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('a', class_='avatar')
    links = [link.attrs["href"] for link in titles]
    data = []
    for link in links:
        news = requests.get(baseUrl + link)
        soup = BeautifulSoup(news.content, "html.parser")
        if not soup.find("h1", {"class": "title"}):
            continue

        abstract = soup.find("h2", {'class': 'sapo'}).text
        abstract = abstract.replace("/\r/\n", abstract).strip()

        title = soup.find("h1", {"class": "title"}).text
        title = title.replace("/\r/\n", title).strip()

        body = soup.find("span", id="mainContent")
        content = ""
        check = len(list(body.findChildren("p", recursive=False)))
        try:
            for i in range(check):
                content += body.findChildren("p", recursive=False)[
                    i].text
        except:
            content = ""

        if not body.find("img"):
            continue

        image = body.find("img").attrs["src"]

        data.append({
            "title": title,
            "abstract": abstract,
            "content": content,
            "image": image,
        })
        print("======POST========")
        requests.post("http://13.214.56.12/api/create-post", {
            "title": title,
            "content": content,
            "image": image,
            "link": link,
            "baseUrl": baseUrl
        })
    return data


if __name__ == "__main__":
    sources = [{"type": "cafef", "base": "https://cafef.vn",
               "link": "https://cafef.vn/thi-truong-chung-khoan.chn"}, {"type": "tuoitre", "base": "https://tuoitre.vn", "link": "https://tuoitre.vn/kinh-doanh/dau-tu.htm"}]
    # sources = [{"base": "https://tuoitre.vn",
    #            "link": "https://tuoitre.vn/tin-moi-nhat.htm"}]
    for source in sources:
        if source["type"] == "cafef":
            crawCafeF(source['base'], source['link'])
        elif source["type"] == 'tuoitre':
            crawNewsData(source['base'], source['link'])

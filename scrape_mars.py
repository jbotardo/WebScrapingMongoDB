from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests


def scrape():
    mars_data = {}
    output = scrape_info()

    mars_data.update({
        "title":output["news_title"],
        "paragraph":output["news_p"],
        "img":scrape_images(),
        "weather":scrape_twitter(),
        "facts":scrape_facts(),
        "hemisphere":scrape_hemisphere()
    })

    return mars_data

# def init_browser():
#     executable_path = {"executable_path": "chromedriver.exe"}
#     browser = Browser('chrome', **executable_path, headless=False)

# collect the latest News Title and Paragraph Text


def scrape_info():
    browser = Browser("chrome")

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()

    # store data in dictionary
    nasa_data = {
        "news_title": news_title,
        "news_p": news_p
    }

    # close the browser
    browser.quit()

    return nasa_data


# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string
def scrape_images():
    browser = Browser("chrome")

    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    query_url = 'https://www.jpl.nasa.gov'
    relative_image_path = soup.find('article')['style'].\
        replace('background-image: url(', '').replace(');', '')[1:-1]

    featured_img_url = query_url + relative_image_path

    browser.quit()
    return featured_img_url


# scrape the latest Mars weather tweet from the page
def scrape_twitter():
    browser = Browser("chrome")

    url_3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_3)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find(
        "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    browser.quit()
    return mars_weather


# use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc
# Use Pandas to convert the data to a HTML table string
def scrape_facts():
    # browser = Browser("chrome")

    url_4 = "https://space-facts.com/mars/"
    tables = pd.read_html(url_4)
    df = tables[0]
    df.columns = ["description", "value"]
    df.set_index('description', inplace=True)

    fact_table = df.to_html()
    fact_table = fact_table.replace("\n", "")

    return fact_table


# obtain high resolution images for each of Mar's hemispheres.
def scrape_hemisphere():
    browser = Browser("chrome")

    url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_5)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []
    # find titles and links
    hemispheres = soup.find_all("div", class_="item")
    for hemis in hemispheres:
        title = hemis.find('h3').text
        class_url = hemis.find("a", class_="itemLink product-item")["href"]

        combined_url = "https://astrogeology.usgs.gov/" + class_url
        browser.visit(combined_url)
        html = browser.html
        soup = bs(html, "html.parser")

        img_url = url_5 + soup.find("img", class_="wide-image")['src']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    browser.quit()
    return hemisphere_image_urls

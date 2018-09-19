
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import tweepy


# Twitter API Keys
from config import (consumer_key, consumer_secret,
                    access_token, access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# Function to new page for image url
def scrapeNEW(newURL):

    # Initialize browser
    browser = init_browser()

    # Visit new url
    browser.visit(newURL)

    # Scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find original image
    downloads = soup.find('div', class_='downloads')
    # Return results
    return (downloads.find_all('a')[1]['href'])


def MarsNews():
    # Initialize browser
    browser = init_browser()
    # *** MARS NEWS ***
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Scrape the NASA Mars News Site and collect the
    # latest News Title and Paragraph Text.
    # Assign the text to variables that you can reference later.
    LatestTitle = soup.find('li', class_='slide').\
        find('div', class_='content_title').get_text()
    LatestPara = soup.find('li', class_='slide').\
        find('div', class_='article_teaser_body').get_text()
    News = {"Title": LatestTitle,
            "SubPara": LatestPara}
    return News


# *** MARS SPACE IMAGES ***
def MarsSpaceImage():
    # Initialize browser
    browser = init_browser()
    # JPL Featured Space Image
    baseURL = 'https://www.jpl.nasa.gov'
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Use splinter to navigate the site and find the image url for the current
    # Featured Mars Image and assign the url string to a variable called
    # featured_image_url.
    image_url1 = soup.find('article')['style']
    image_url2 = image_url1.split("'")
    featured_image_url = baseURL + image_url2[1]
    return featured_image_url


# *** MARS WEATHER ***
def MarsWeather():
    # Mars Twitter
    target = '@MarsWxReport'
    # Get all tweets from home feed
    public_tweets = api.user_timeline(target)
    # Loop through all tweets
    for tweet in public_tweets:
        if (tweet['text'].startswith("Sol")):
            mars_weather = tweet['text']
            break
    return mars_weather


# *** MARS FACTS ***
def MarsFacts():
    # Initialize browser
    browser = init_browser()
    # Mars Fact URL
    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    # Visit the Mars Facts webpage here and use Pandas to
    # scrape the table containing facts
    # about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(url)
    return tables


# *** MARS HEMISPHERES ***
def MarsHemi():
    # Initialize browser
    browser = init_browser()
    # Visit the USGS Astrogeology site here to obtain high resolution
    # images for each of Mar's hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+\
        enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    baseURL = 'https://astrogeology.usgs.gov'
    test = soup.find_all('div', class_='item')
    for i in range(4):
        link_data = {}
        title = (test[i].find('h3').get_text())
        newURL = (baseURL + test[i].find('a')['href'])
        # scrape new page for image url
        img_url = scrapeNEW(newURL)
        link_data['title'] = title
        link_data['img_url'] = img_url
        hemisphere_image_urls.append(link_data)

    return hemisphere_image_urls

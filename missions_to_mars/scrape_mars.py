# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Define scrape function
def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # ----- 1.) Scrape Mars news site -----
    # Use splinter browser variable to navigate to the mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Use div with class 'content_title' to find list of all news titles
    article_titles = soup.find_all('div', class_='content_title')
    # Pull first one to get latest title
    latest_article_title = article_titles[0].text
    # Use div with class 'article_teaser_body' to find list of news paragraph text
    article_paragraphs = soup.find_all('div', class_='article_teaser_body')
    # Pull first one to get latest article paragraph
    latest_article_paragraph = article_paragraphs[0].text
    # -------------------------------------

    # Store data in a dictionary
    mars_data = {
        "latest_article_title": latest_article_title,
        "latest_article_paragraph": latest_article_paragraph,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
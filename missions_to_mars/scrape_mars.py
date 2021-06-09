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

    # ----- 2.) Scrape Mars featured image site -----
    # Use splinter browser variable to navigate to the mars news site
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Use div with class 'content_title' to find list of all news titles
    featured_image = soup.find('img', class_='headerimage')
    # Pull first one to get latest title
    featured_image_url =  url + featured_image['src']
    # -------------------------------------

    # ----- 3.) Use pandas to scrape Mars Facts table -----
    # Define url for pandas to scrape
    url = 'https://galaxyfacts-mars.com/'
    # Read in tables from url defined above
    tables = pd.read_html(url)
    # Convert list returned above into dataframe
    table_df = tables[0]
    # Rename columns and reset index
    table_df.columns = table_df.iloc[0]
    table_df = table_df.drop(table_df.index[0])
    # Output scraped dataframe to html string
    table_html_string = table_df.to_html(index=False).replace('\n', '')
    # Replace table tag with bootstrap class rather than generated html from pandas
    table_html_string = table_html_string.replace('<table border="1" class="dataframe">','<table class="table table-striped">')
    # -------------------------------------

    # ----- 4.) Scrape Mars hemispheres site and pull full resolution image paths -----
    # Use splinter to navigate to URL to scrape images from
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # Scrape using BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create empty list to store hemisphere image urls
    hemisphere_image_urls = []

    # USE BELOW FOR CLICKING - BELOW WORKS
    image_links = browser.find_by_css('a.product-item h3')

    for i in range(0,len(image_links)-1):
        # Reset variable to avoid "StaleReferenceException"
        # Approach adapted from https://www.selenium.dev/exceptions/#stale_element_reference
        image_to_click = browser.find_by_css('a.product-item h3')[i]
        # Pull title and remove 'Enhanced' from title name
        title = image_to_click.text
        title_final = title.replace(" Enhanced","")
        # Use splinter to navigate to the a tag destination, then scrape for the full resolution image path
        image_to_click.click()
        # Now that we are on new page, reset html and soup variables
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # Scrape the full resolution image path
        image_path = soup.find('img',class_='wide-image')['src']
        # Put title and image path in dictionary, and add to hemisphere_image_urls list created above
        image_url_dict = {'title':title_final,'img_url':url + image_path}
        hemisphere_image_urls.append(image_url_dict)
        # Navigate back to original page to scrape the next image
        browser.links.find_by_partial_text('Back').click()
        time.sleep(1)
    # -------------------------------------

    # Store data in a dictionary
    mars_data = {
        "latest_article_title": latest_article_title,
        "latest_article_paragraph": latest_article_paragraph,
        "featured_image_url":featured_image_url,
        "table_html_string":table_html_string,
        "hemisphere_image_urls":hemisphere_image_urls,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time

# Initialize browser
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    
    # ------ NASA Mars News ----------------------------------
    url = "https://mars.nasa.gov/news/"   
    browser.visit(url)

    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Get the latest news title and paragraph text
    article = soup.find('div', class_='list_text')
    news_title = article.find('a').text
    news_p = article.find('div', class_='article_teaser_body').text

    # browser.quit()

    #browser = init_browser()
    
    # ------- JPL Mars Space Images - Featured Image ----------
    nasa_url = "https://www.jpl.nasa.gov"
    jpl_query = "/spaceimages/?search=&category=Mars"
    browser.visit(nasa_url+jpl_query)

    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Find the image url for the current Featured Mars Image
    article = soup.find('div', class_='carousel_items').find('article')
    featured_image_url = article['style'].split("'")[1]
    jpl_image_url = nasa_url+featured_image_url

    #browser.quit()


    # ------- Mars Facts ---------------------------------------
    
    #browser = init_browser()

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(1)
    
    # Read html using pandas
    html = browser.html
    tables = pd.read_html(html)
    
    # Scrape the table containing facts about the planet including Diameter, Mass, etc.
    df = pd.DataFrame(tables[0])
    table_html = df.to_html(index=False, border=1, header=False, 
                            classes=["table", "table-responsive", "table-striped"], 
                            justify='center')

    #browser.quit()

    # ------------- Mars Hemisphere images -----------------

    # browser = init_browser()
    
    # Visit the url for JPL Featured Space Image
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Find all items
    items = soup.find_all('div', class_='item')
    
    # Initialize a list
    hemisphere_image_urls = []
    
    # Find the titles and image urls for the Hemispheres
    usgs_url = "https://astrogeology.usgs.gov"
    for item in items:
        # Find title of this item
        title = item.find('h3').text
        
        # Initialize a dictionary
        hemisphere = {}
        
        # Find the url where this item is explained in detail
        item_url = item.find('a')['href']
        
        # Click the link of each item
        browser.find_by_text(title).click()
        soup2 = bs(browser.html, "html.parser")
        
        # Find the link for the full size image - the first link is for jpg, and the 2nd is tif(full size)
        imgs = soup2.find('div', class_="downloads").find_all('a')
        jpg_url = imgs[0]['href']
        
        # Add the img url to the dictionary
        hemisphere['title'] = title
        hemisphere['img_url'] = jpg_url
        
        # Append the dictionary to the list
        hemisphere_image_urls.append(hemisphere)
        
        # Back to the USGS Astrogeology site
        browser.back()

    # Quit the browser
    browser.quit()

    return {
        'news_title': news_title, 
        'news_p': news_p,
        'jpl_img' : jpl_image_url,
        'facts_table' : table_html,
        'Hemisphere_imgs' : hemisphere_image_urls
    }

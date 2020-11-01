# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape_all():
    browser = init_browser()
    #-------------Mars News--------------
    # To scrape the URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # To scrape page create soup
    html = browser.html
    soup = bs(html, "html.parser")

    # to avoid lag time
    time.sleep(2)
    
        
    # Get the latest news title and paragraph text
    article = soup.find('div', class_='list_text')
    news_title = article.find('a').text
    news_p = article.find('div', class_='article_teaser_body').text



    #-------------JPL Mars Space Images - Featured Image --------------
    # To set up url to scrape image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Marsa"

    # To grab image from url 
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Marsa'

    browser.visit(featured_image_url)

    time.sleep(2)

    html = browser.html

    images_soup = bs(html, 'html.parser')
    # To retrieve the featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_url + relative_image_path


    #-------------Mars Facts --------------
    # To set up url to scrape mars facts
    mars_url = "https://space-facts.com/mars/"

    browser.visit(mars_url)

    time.sleep(2)

    # To read html using pandas
    mars_html = browser.html
    tables = pd.read_html(mars_html)
   
    # To show in dataframe table
    df = pd.DataFrame(tables[2])

    # To rename columns
    df.columns = ["Description", "Value"]

    # To reindex columns
    df = df.set_index("Description")
    
    # To scrape the table with the facts about mars to include: diameter, mass, etc.
    table_html = df.to_html(index=False, border=1, header=False,
                        classes=["table","table-responsive","table-striped"],
                        justify='center')
    # To clean data output by removing \n
    table_html.replace('\n', '')

    #-------------Mars Hemispheres--------------
    # To set up url to scrape hemisphere name and image
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_url = 'https://astrogeology.usgs.gov'
    browser.visit(hem_url)

    time.sleep(2)

    hem_html = browser.html

    hem_soup = bs(hem_html, 'html.parser')

    # To find hemisphere data in page
    total_data = hem_soup.find('div', class_='collapsible results')
    mars_hemispheres = total_data.find_all('div', class_='item')

    # To initialize a list
    hemisphere_image_urls = []

# To find the titles and image urls for the Hemisphere iterate through each hemisphere's data
    for i in mars_hemispheres:
        # To collect the titles
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # To collect image links by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # To create dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)

# To put data into dictionary
    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "fact_table": str(table_html),
            "hemisphere_images": hemisphere_image_urls
        }
    #To quit the browswer
    browser.quit()

    return mars_dict
    
    #To initialize the main scrape function
if __name__ == "__main__":  
    scrape_all()
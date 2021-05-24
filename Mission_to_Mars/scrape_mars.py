from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():
    browser = init_browser()
    listings = {}

    # Visit redplanetscience.com/
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    listings["title"] = soup.find('div', class_="content_title").get_text()
    listings["paragraph"] = soup.find('div', class_="article_teaser_body").get_text()

    # Close the browser after scraping
    browser.quit()

    return listings

def scrape_spaceimages():
    browser = init_browser()
    

    # Visit spaceimages-mars.com
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #used https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948 for ['src']
    featured_image_url = 'https://spaceimages-mars.com/'+soup.find('img', class_="headerimage fade-in")['src']

    # Close the browser after scraping
    browser.quit()

    return featured_image_url

def scrape_facts():
    browser = init_browser()
    #tables[0] has Diameter and Mass so it's the one we're looking for
    tables = pd.read_html('https://galaxyfacts-mars.com/')
    df = tables[0]

    html_table = df.to_html(header = False, index = False)
    
    # Close the browser after scraping
    browser.quit()

    return html_table
    
def scrape_hemispheres():
    browser = init_browser()

    # Visit marshemispheres.com
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html

    #this entire block of code was written with the help of askBCS
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')
    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        # Finally, we navigate backwards
        browser.back()


    # Close the browser after scraping
    browser.quit()

    return hemisphere_image_urls

def scrape():
    news = scrape_news()
    img_url = scrape_spaceimages()
    facts = scrape_facts()
    hemisphere_image_urls = scrape_hemispheres()

    data = {
        "title": news["title"],
        "paragraph": news["paragraph"],
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
    }
    return data 

if __name__ == "__main__":
    print(scrape())
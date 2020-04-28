def scrape():

    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    import requests as r
    import time

    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)  
    mars = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find("div", class_ = "content_title").text
    news_p = soup.find("div", class_ = "article_teaser_body").text
    print(f"news_title = {news_title}")
    print(f"news_p = {news_p}")
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_p 

    ##Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")
    image_url = soup.select_one("figure.lede a img").get("src")
    #print(image_url)
    featured_image_url = "https://www.jpl.nasa.gov"+image_url
    #print(featured_image_url)
    mars['featured_image_url'] = featured_image_url

    #Mars Weather
    url_3 = "https://twitter.com/marswxreport?lang=en"
    response = r.get(url_3)
    soup =BeautifulSoup(response.text, "html.parser")
    #print(soup.prettify())
    tweet = soup.find('div', class_="js-tweet-text-container").text.strip()
    mars["tweet"] = tweet
    #print(tweet)

    #Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    facts_table[0]
    facts_df = facts_table[0]
    facts_df.columns = ['Paramter','Value']
    facts_df.set_index('Paramter', inplace=True)
    facts_df.head()
    facts_html_table = facts_df.to_html()
    facts_html_table
    facts_html_table = facts_html_table.replace('\n', '')
    mars["facts_table"] = facts_html_table

    # Mars Hemispheres

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    response = r.get(hemisphere_url)
    soup = BeautifulSoup(response.text, 'html.parser').find_all("a",class_ = "itemLink product-item")
    hemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov'
    for i in soup:
        title = i.find("h3").text
        url=i.find("img")["src"]
        img_url = base_url + url
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    
    hemisphere_image_urls
    mars["hemisphere_image_urls"] = hemisphere_image_urls
    print(mars)

    return mars


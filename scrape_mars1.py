from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import os
import app


#scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["news_title"] = output[0]
    final_data["mars_news"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    #return final_data

def marsNews():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    featured_img_base = "https://www.jpl.nasa.gov"
    featured_img_url_raw = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_img_url_raw.split("'")[1]
    featured_img_url = featured_img_base + featured_img_url
    #return featured_image_url

def marsWeather():
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    for weather in latest_tweets: 
        mars_weather = weather.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
        break
    else:
                pass
    #return mars_weather

def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data_df = pd.DataFrame(mars_data[0])
    mars_facts = mars_data_df.to_html(header = False, index = False)
    #return mars_facts

def marsHem():
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src'] 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    #return hemisphere_image_urls
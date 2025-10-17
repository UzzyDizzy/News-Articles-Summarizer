# utils/fetch_news.py
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup, BeautifulSoup
from PIL import Image
import streamlit as st
import io
from newspaper import Article
import urllib.parse
import requests  # missing import
import logging

logging.basicConfig(level=logging.DEBUG)

def test_network_and_parse_article(url, html=None):
    # First, let's check if the network is accessible
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logging.debug(f"Network access successful: {url}")
        else:
            logging.error(f"Failed to access {url}, Status Code: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        logging.error(f"Network timeout while accessing {url}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while accessing {url}: {e}")
        return None
    
    # Now, try to fetch and parse the article using newspaper
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        logging.debug(f"Article title: {article.title}")
        return {
            'summary': article.summary,
            'top_image': article.top_image,
            'title': article.title,
        }
    except Exception as e:
        logging.error(f"Error parsing article: {e}")
        return None

@st.cache_data(ttl=3600)
def fetch_news_by_topic_country(topic=None, country="in"):
    if topic:
        site = f"https://news.google.com/rss/search?q={topic}&hl=en-{country.upper()}&gl={country.upper()}&ceid={country.upper()}:en"
    else:
        site = f"https://news.google.com/rss?hl=en-{country.upper()}&gl={country.upper()}&ceid={country.upper()}:en"
    
    try:
        response = urlopen(site)
        xml_data = response.read()
        parsed = soup(xml_data, 'xml')
        news_items = parsed.findAll('item')

        news_list = []
        for item in news_items:
            news_list.append({
                'title': item.title.text if item.title else '',
                'link': item.link.text if item.link else '',
                'pubDate': item.pubDate.text if item.pubDate else '',
                'source': item.source.text if item.source else '',
                'description': item.description.text if item.description else '',
            })

        return news_list

    except Exception as e:
        print("Error fetching news:", e)
        return []

@st.cache_data(ttl=3600)
def fetch_news_by_query(query):
    site = f"https://news.google.com/rss/search?q={query}"
    
    try:
        response = urlopen(site)
        xml_data = response.read()
        parsed = soup(xml_data, 'xml')
        news_items = parsed.findAll('item')

        news_list = []
        for item in news_items:
            news_list.append({
                'title': item.title.text if item.title else '',
                'link': item.link.text if item.link else '',
                'pubDate': item.pubDate.text if item.pubDate else '',
                'source': item.source.text if item.source else '',
                'description': item.description.text if item.description else '',
            })

        return news_list

    except Exception as e:
        print("Error fetching search results:", e)
        return []

@st.cache_data(ttl=3600)
def fetch_news_poster(link):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(link, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        og_image = soup.find("meta", property="og:image")
        twitter_image = soup.find("meta", property="twitter:image")
        img_tag = soup.find("img")

        if og_image and og_image.get("content"):
            return og_image["content"]
        elif twitter_image and twitter_image.get("content"):
            return twitter_image["content"]
        elif img_tag and img_tag.get("src"):
            return img_tag["src"]
        else:
            return None

    except Exception as e:
        print(f"Error fetching poster: {e}")
        return None

@st.cache_data(ttl=3600)
def parse_article_with_newspaper(url, html=None):
    from newspaper import Article

    try:
        article = Article(url)
        if html:
            article.set_html(html)   # use provided HTML instead of downloading
            article.parse()
        else:
            article.download()
            article.parse()
        article.nlp()

        return {
            'summary': article.summary,
            'top_image': article.top_image,
            'title': article.title,
        }
    except Exception as e:
        print(f"Error parsing article: {e}")
        return None

@st.cache_data(ttl=3600)
def display_news(news_list, count):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import time

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    for idx, news in enumerate(news_list[:count], 1):
        st.write(f"**({idx}) {news['title']}**")

        # Step 1: Use Selenium to get final URL
        try:
            driver.get(news['link'])
            time.sleep(1)
            final_url = driver.current_url
            html = driver.page_source
        except Exception as e:
            st.warning(f"⚠️ Failed to open link with Selenium: {e}")
            continue

        # Step 2: Use newspaper3k on final URL
        parsed = test_network_and_parse_article(final_url, html=html)
        logging.debug(f"Output: {parsed}")
        if not parsed:
            st.error("❌ Failed to parse article.")
            continue

        # Step 3: Poster fetching logic
        poster = parsed['top_image'] or fetch_news_poster(final_url)
        if poster:
            try:
                st.image(poster, use_container_width=True)
            except Exception as e:
                st.warning(f"⚠️ Image render failed: {e}")
        else:
            st.info("⚠️ No poster image found.")

        # Step 4: Display summary and link
        with st.expander(parsed['title'] or news['title']):
            st.markdown(f"<h6 style='text-align: justify;'>{parsed['summary']}</h6>", unsafe_allow_html=True)
            st.markdown(f"[Read more at {news['source']}]({news['link']})")

        st.success("Published Date: " + news['pubDate'])

    driver.quit()
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
    try:
        if not html:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text
        
        # Try newspaper first
        result = parse_article_with_newspaper(url, html)
        if result:
            return result
            
        # Fallback to readability
        from readability import Document
        doc = Document(html)
        return {
            'summary': doc.summary(),
            'top_image': None,
            'title': doc.title(),
        }
        
    except Exception as e:
        st.error(f"All parsing methods failed: {e}")
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
    import time
    
    for idx, news in enumerate(news_list[:count], 1):
        st.write(f"**({idx}) {news['title']}**")

        # Step 1: Use requests to get final URL (no Selenium)
        try:
            response = requests.get(news['link'], timeout=10, allow_redirects=True)
            final_url = response.url
            html = response.text
        except Exception as e:
            st.warning(f"⚠️ Failed to open link: {e}")
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
            st.markdown(f"[Read more at {news['source']}]({final_url})")  # Use final_url

        st.success("Published Date: " + news['pubDate'])
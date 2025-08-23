# utils/widgets.py

import streamlit as st
from utils.fetch_news import fetch_news_by_topic_country, display_news

def create_sidebar_filters():
    st.sidebar.title("🔍 Filters")

    num_articles = st.sidebar.slider("📊 Number of Articles", 5, 25, 10)

    country_options = {
        'United States': 'us',
        'United Kingdom': 'gb',
        'Canada': 'ca',
        'Australia': 'au',
        'Germany': 'de',
        'France': 'fr',
        'Japan': 'jp',
        'India': 'in',
        'Brazil': 'br',
        'South Africa': 'za'
    }
    selected_country_name = st.sidebar.selectbox("🌍 Country", list(country_options.keys()))
    selected_country = country_options[selected_country_name]

    category = ['--Select--', 'Trending News🔥', 'Favourite Topics💙']
    cat_op = st.sidebar.selectbox('🏷️ Category', category)

    chosen_topic = None

    if cat_op == category[0]:
        st.warning('Please select a category.')

    elif cat_op == category[1]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = num_articles
        news_list = fetch_news_by_topic_country(country=selected_country)
        display_news(news_list, no_of_news)

    elif cat_op == category[2]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please choose a topic.")
        else:
            no_of_news = num_articles
            news_list = fetch_news_by_topic_country(topic=chosen_topic, country=selected_country)
            if news_list:
                st.subheader(f"✅ Some {chosen_topic} News for you")
                display_news(news_list, no_of_news)
            else:
                st.error(f"No News found for {chosen_topic}")

    # ✅ Clean return for app.py
    category_value = chosen_topic.upper() if chosen_topic else None
    return {
        'num_articles': num_articles,
        'country': selected_country.upper(),
        'country_name': selected_country_name,
        'category': category_value
    }

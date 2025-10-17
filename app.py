# app.py
import streamlit as st
from datetime import datetime
import nltk
nltk.download('punkt')

from utils.fetch_news import fetch_news_by_query, fetch_news_by_topic_country, display_news
from utils.widgets import create_sidebar_filters

st.set_page_config(
    page_title="Newstrackr - News Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    if 'news_data' not in st.session_state:
        st.session_state.news_data = []
    if 'last_fetch_time' not in st.session_state:
        st.session_state.last_fetch_time = None
    if 'current_filters' not in st.session_state:
        st.session_state.current_filters = {}
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""

def load_news_data(filters):
    current_time = datetime.now()
    if (st.session_state.last_fetch_time is None or 
        (current_time - st.session_state.last_fetch_time).seconds > 3600 or
        st.session_state.current_filters != filters):
        
        with st.spinner("🔄 Fetching latest news..."):
            articles = fetch_news_by_topic_country(
                topic=filters['category'],
                country=filters['country']
            )
            st.session_state.news_data = articles
            st.session_state.last_fetch_time = current_time
            st.session_state.current_filters = filters.copy()
    
    return st.session_state.news_data

def main():
    initialize_session_state()

    st.markdown("""
    <div class="main-header">
        <h1>📰 Newstrackr</h1>
        <p>AI-Powered News Summarizer</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("## ⚙️ Configuration")
    
    # 🔥 Search input (global control)
    user_topic = st.text_input("🔎 Search News", value=st.session_state.search_query)

    # 🔁 If search is entered, reset filters
    if user_topic.strip():
        st.session_state.search_query = user_topic.strip()
        st.session_state.last_fetch_time = None  # ensure fresh fetch
        filters = {'country': 'US', 'category': None, 'num_articles': 10}
        news_list = fetch_news_by_query(query=st.session_state.search_query)

        if news_list:
            st.subheader(f"✅ Here is some '{st.session_state.search_query}' News for you")
            display_news(news_list, 10)
        else:
            st.error(f"No News found for {st.session_state.search_query}")
        return  # ⛔ Stop here if search was used

    # If no search → show filters
    st.session_state.search_query = ""  # 🧹 Reset search when using filters

    filters = create_sidebar_filters()

    if st.sidebar.button("🔄 Refresh News"):
        st.session_state.last_fetch_time = None
        st.rerun()

    if st.session_state.last_fetch_time:
        st.sidebar.info(f"Last updated: {st.session_state.last_fetch_time.strftime('%H:%M:%S')}")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🤖 AI Models Used")
        st.markdown("- **Summarizer**: newspaper3k")

    with col2:
        st.markdown("### 📊 Data Sources")
        st.markdown("- **News**: Google News RSS")

    with col3:
        st.markdown("### 🔄 Caching")
        st.markdown("- News data: 1 hour cache\n- Summaries: Cached per article")

if __name__ == "__main__":
    main()

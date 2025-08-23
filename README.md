
# 📰 Newstrackr

**Newstrackr** is an AI-powered News Summarization app built with **Streamlit**. It fetches real-time news from Google News RSS, summarizes the articles using `newspaper3k`, and ranks them using relevance and impact. Users can filter news by country, category, or search for custom topics.

---

## 🚀 Features

- 🔎 **Search Functionality**: Search for news on any topic.
- 🌍 **Country-Based Filtering**: Choose from countries like US, UK, India, Germany, etc.
- 🏷️ **Category-Based Filters**: Trending news or favorite topics (e.g., Tech, Health, Sports).
- 🧠 **AI Summarizer**: Uses `newspaper3k` for intelligent news summarization.
- 🖼️ **Poster Images**: Automatically fetches featured images from articles.
- ⚡ **Smart Caching**: 1-hour cache for efficient performance.
- 🌐 **Live URL Parsing**: Uses Selenium to access the actual news URL before summarizing.
- 📱 **Responsive UI**: Clean and modern layout using Streamlit.

---

## 🧩 Project Structure

```
Newstrackr/
│
├── app.py                        # Main Streamlit app
├── requirements.txt              # Project dependencies
├── README.md                     # Project documentation
└── utils/
    ├── fetch_news.py             # Fetching, parsing, summarizing news
    └── widgets.py                # UI sidebar filters and layout
```

---

## 🛠️ Installation

### 📌 Prerequisites

- Python 3.7+
- Chrome browser installed
- ChromeDriver (matching your browser version)

> Optional: Use `webdriver-manager` to manage drivers dynamically

---

### ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/UzzyDizzy/newstrackr.git
   cd newstrackr
   ```

2. **Create Python Virtual Environment**:
   ```bash
   python -m venv myenv       #create python virtual environment
   myenv\Scripts\activate     #activate python virtual environment
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Example Usage

- **Search** for `"AI in Healthcare"` in the search bar.
- Or select:
  - Country: `India`
  - Category: `Favourite Topics` → `TECHNOLOGY`
- View summarized results with:
  - Headline
  - Poster image
  - Bullet summary
  - Link to full article
  - Published date

---

## 📦 Dependencies

- `streamlit`
- `nltk`
- `beautifulsoup4`
- `requests`
- `newspaper3k`
- `pillow`
- `selenium`
- `lxml`
- `urllib3`

---

## 🛡️ Notes

- This app uses **Selenium + newspaper3k** to ensure articles are parsed from their **final URLs** (not RSS redirects).
- All article summaries are generated on-the-fly and cached.
- Image fetching uses `Open Graph`, `Twitter card`, or `<img>` fallback.

---

## ✨ To-Do (Future Features)

- Impact-based news ranking using Twitter metrics.
- User authentication & personalized feed.
- Save/share summarized articles.
- Dark mode toggle.

---

## 📃 License

MIT License. Free for personal and educational use.

---

## 👨‍💻 Author

Made with ❤️ by [UzzyDizzy](https://github.com/UzzyDizzy)

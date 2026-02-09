import requests
from bs4 import BeautifulSoup
import re
import time

def scrap_text(pages=50):
    base_url = "https://vnexpress.net/tin-tuc-24h"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    sentences_list = []

    print(f"🚀 Starting scraper for {pages} pages...")

    for p in range(1, pages + 1):
        try:
            # 1. Get the list of articles on the page
            res = requests.get(f"{base_url}{p}", headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = [a['href'] for a in soup.select('h3.title-news a') if 'href' in a.attrs]

            for link in links:
                # 2. Visit each article
                article_res = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(article_res.text, 'html.parser')
                
                # VnExpress articles usually store text in <p class="description"> and <p class="Normal">
                paragraphs = article_soup.select('p.description, p.Normal')
                for p_tag in paragraphs:
                    text = p_tag.get_text().strip()
                    # Split into sentences based on dots followed by space
                    parts = re.split(r'(?<=[.!?]) +', text)
                    for s in parts:
                        if len(s) > 15 and len(s) < 100: # Filter for OCR-friendly lengths
                            sentences_list.append(s)
                
                time.sleep(0.1) # Be polite to their servers
            print(f"✅ Finished page {p}. Total sentences: {len(sentences_list)}")
        except Exception as e:
            print(f"⚠️ Error on page {p}: {e}")

    # 3. Save to file
    with open("vn_corpus.txt", "w", encoding="utf-8") as f:
        for s in list(set(sentences_list)): # Use set() to remove duplicates
            f.write(s + "\n")
    
    print(f"🏁 Done! Saved {len(sentences_list)} unique sentences to vn_corpus.txt")

# Run it
scrap_vnexpress(pages=30)
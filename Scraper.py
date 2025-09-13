# scraper_playwright.py
import sqlite3
import pandas as pd
from playwright.sync_api import sync_playwright

DB_NAME = "ecommerce.db"
TABLE_NAME = "products"

# ---------- DB Save & Clean ----------
def save_raw_to_db(df, reset=False):
    if df is None or df.empty:
        return
    conn = sqlite3.connect(DB_NAME)
    if reset:
        conn.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    conn.close()

def clean_and_update_db():
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
    except:
        conn.close()
        return
    if df.empty:
        conn.close()
        return
    # Clean price & rating
    df["Price"] = df["Price"].astype(str).str.replace("₹", "").str.replace(",", "").str.extract(r"(\d+)")[0]
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"].astype(str).str.extract(r"(\d+\.\d+)")[0], errors="coerce")
    df = df.dropna(subset=["Price"])
    df["Price"] = df["Price"].astype(float)
    conn.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    conn.close()


# ---------- Amazon ----------
def scrape_amazon(query, max_pages=1):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.amazon.in/s?k={query.replace(' ','+')}")
        for _ in range(max_pages):
            items = page.query_selector_all("div[data-component-type='s-search-result']")
            for item in items:
                try:
                    title = item.query_selector("h2").inner_text()
                except: continue
                try:
                    price = item.query_selector(".a-price-whole").inner_text()
                except: price = "N/A"
                try:
                    rating = item.query_selector(".a-icon-alt").inner_text()
                except: rating = "N/A"
                try:
                    link = item.query_selector("a").get_attribute("href")
                except: link = ""
                products.append({"Source":"Amazon","Title":title,"Price":price,"Rating":rating,"Link":link})
            try:
                next_btn = page.query_selector("a.s-pagination-next")
                if next_btn:
                    next_btn.click()
                    page.wait_for_timeout(2000)
                else:
                    break
            except:
                break
        browser.close()
    return pd.DataFrame(products)


# ---------- Myntra ----------
def scrape_myntra(query, max_pages=1):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.myntra.com/{query.replace(' ','-')}")
        for _ in range(max_pages):
            items = page.query_selector_all(".product-base")
            for item in items:
                try:
                    brand = item.query_selector(".product-brand").inner_text()
                    name = item.query_selector(".product-product").inner_text()
                    title = f"{brand} {name}"
                except: continue
                try:
                    price = item.query_selector(".product-price").inner_text()
                except: price = "N/A"
                try:
                    link = item.query_selector("a").get_attribute("href")
                except: link = ""
                products.append({"Source":"Myntra","Title":title,"Price":price,"Rating":"N/A","Link":link})
            try:
                next_btn = page.query_selector("li.pagination-next a")
                if next_btn:
                    next_btn.click()
                    page.wait_for_timeout(2000)
                else:
                    break
            except:
                break
        browser.close()
    return pd.DataFrame(products)


# ---------- Flipkart ----------
def scrape_flipkart(query, max_pages=1):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.flipkart.com/search?q={query.replace(' ','+')}")
        for _ in range(max_pages):
            titles = page.query_selector_all(".IRpwTa, ._4rR01T")
            prices = page.query_selector_all("._30jeq3")
            links = page.query_selector_all("a._1fQZEK, a.IRpwTa")
            for i in range(min(len(titles), len(prices), len(links))):
                products.append({"Source":"Flipkart","Title":titles[i].inner_text(),
                                 "Price":prices[i].inner_text(),"Rating":"N/A",
                                 "Link":links[i].get_attribute("href")})
            try:
                next_btn = page.query_selector("a._1LKTO3")
                if next_btn:
                    next_btn.click()
                    page.wait_for_timeout(2000)
                else:
                    break
            except:
                break
        browser.close()
    return pd.DataFrame(products)


# ---------- Run Scrapers ----------
def run_scrapers_and_update_db(query, use_amazon=False, use_myntra=False, use_flipkart=False, max_pages=1):
    reset = True
    if use_amazon:
        save_raw_to_db(scrape_amazon(query, max_pages), reset=reset)
        reset = False
    if use_myntra:
        save_raw_to_db(scrape_myntra(query, max_pages), reset=reset)
        reset = False
    if use_flipkart:
        save_raw_to_db(scrape_flipkart(query, max_pages), reset=reset)
        reset = False
    clean_and_update_db()

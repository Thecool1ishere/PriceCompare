import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus
from selenium.webdriver.chrome.options import Options
st.title("Price Comparison for Products on Flipkart, Micro Center, Best Buy, and Newegg")

options = Options()


options.add_argument("--headless=new")


options.add_argument("--no-sandbox")


options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=options)


dict1 = {}


def flipkartscrap(product):
    wait = WebDriverWait(driver, 15)
    search_url = f"https://www.flipkart.com/search?q={quote_plus(product)}"
    driver.get(search_url)

    try:
        price_element = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//div[@data-id]//*[contains(text(), '₹') and not(self::span)])[1]",
                )
            )
        )

        price_text = price_element.text
        price = int(price_text.replace("₹", "").replace(",", "").strip())

        st.write(f"Price in USD for Flipkart: {price/95.25:.2f}")

        dict1["Flipkart"] = float(f"{price/95.25:.2f}")

    except Exception:
        st.write("Flipkart: Product not found")


def microcenterscrap(product):
    wait = WebDriverWait(driver, 20)

    search_url = (
        f"https://www.microcenter.com/search/search_results.aspx?Ntt={quote_plus(product)}"
    )

    driver.get(search_url)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".product_wrapper")
            )
        )

        price_element = driver.find_element(
            By.XPATH,
            "//span[@itemprop='price']"
        )

        price_text = (
            price_element.get_attribute("content")
            or price_element.text
        )

        price_text = (
            price_text.replace("Our price", "")
            .replace("$", "")
            .replace(",", "")
            .replace("\n", "")
        )

        price_text = float(price_text)

        st.write(f"Price in USD for Micro Center: {price_text}")

        dict1["Micro Center"] = price_text

    except Exception as e:
        st.write(f"Micro Center Error: {e}")


def bestbuyscrap(product):
    wait = WebDriverWait(driver, 20)

    search_url = (
        f"https://www.bestbuy.com/site/searchpage.jsp?st={quote_plus(product)}"
    )

    driver.get(search_url)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".sku-item")
            )
        )

        price_element = driver.find_element(
            By.CSS_SELECTOR,
            ".priceView-customer-price span"
        )

        price_text = price_element.text

        price = float(
            price_text.replace("$", "")
            .replace(",", "")
            .strip()
        )

        st.write(f"Price in USD for Best Buy: {price:.2f}")

        dict1["Best Buy"] = float(f"{price:.2f}")

    except Exception as e:
        st.write(f"Best Buy Error: {e}")


def neweggscrap(product):
    wait = WebDriverWait(driver, 15)

    search_url = f"https://www.newegg.com/p/pl?d={quote_plus(product)}"

    driver.get(search_url)

    try:
        price_element = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//li[contains(@class, 'price-current')]//strong)[1]"
                )
            )
        )

        price_text = price_element.text

        price = float(
            price_text.replace("$", "")
            .replace(",", "")
            .strip()
        )

        st.write(f"Price in USD for Newegg: {price:.2f}")

        dict1["Newegg"] = float(f"{price:.2f}")

    except Exception:
        st.write("Newegg: Product not found")


product = st.text_input(
    "Enter the product you want to search for in Flipkart, Micro Center, and Newegg:"
)

if st.button("Compare Prices"):

    dict1.clear()

    flipkartscrap(product)
    microcenterscrap(product)
    # bestbuyscrap(product)
    neweggscrap(product)

    st.write("### Prices Found")
    st.write(dict1)

    if len(dict1) > 0:

        min_price = min(dict1.values())

        site = ""

        for i in dict1:
            if dict1[i] == min_price:
                site = i

        st.success(
            f"The site with the lowest price is {site} with a price of ${min_price}"
        )

    else:
        st.error("No prices found.")

    driver.quit()

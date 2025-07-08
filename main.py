from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
zillow_web_page_html = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=headers).text

soup = BeautifulSoup(zillow_web_page_html, "html.parser")

anchors = soup.find_all(name="a", class_ = "property-card-link")
urls = []
prices = []
addresses = []

for a in anchors:
    href = a.get("href")
    urls.append(href)

prices_text = soup.find_all(name="span", class_ = "PropertyCardWrapper__StyledPriceLine")
for price in prices_text:
    text = price.text.strip().replace("/", "+")
    cleaned_price = text.split("+")[0]
    prices.append(cleaned_price)

addresses_text = soup.find_all("address")
for address in addresses_text:
    cleaned_address = address.text.strip()
    addresses.append(cleaned_address)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
for n in range(len(urls)):
    sleep(0.5)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfpuzrdzWBtwK1KjFnPUiasbmHeO9awyFdTd2mK-RIKaPwQjw/viewform?hl=en")

    sleep(1.5)
    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

    price_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_input.send_keys(addresses[n])
    price_input.send_keys(prices[n])
    link_input.send_keys(urls[n])
    sleep(0.5)
    submit.click()
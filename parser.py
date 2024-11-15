import json
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

class FundPriceParser:
    def __init__(self, source_name, fund_id, config_file="sources.json"):
        self.source_name = source_name
        self.fund_id = fund_id
        with open(config_file, "r") as f:
            self.config = json.load(f)[source_name]
        self.url = self.config["url_template"].format(fund_id=fund_id)
        self.headers = self.config.get("headers", None)
        self.verify = self.config.get("verify", True)

    def fetch_html(self):
        if self.config["parser_type"] == "javascript":
            return self._fetch_with_playwright()
        else:
            response = requests.get(self.url, headers=self.headers, verify=self.verify)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        
    def _fetch_with_playwright(self):
        # use playwright to render javascript
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)
            page.wait_for_timeout(5000)
            content = page.content()
            browser.close()

        # return the rendered html
        return BeautifulSoup(content, "html.parser")

    def parse_price(self):
        soup = self.fetch_html()
        parser_type = self.config["parser_type"]

        if parser_type == "beautifulsoup":
            return self._parse_with_beautifulsoup(soup)
        elif parser_type == "javascript":
            return self._parse_with_javascript(soup)
        else:
            raise ValueError(f"Unsupported parser type: {parser_type}")

    def _parse_with_beautifulsoup(self, soup):
        find_params = self.config["find_params"]
        element = soup.find(find_params["tag"], attrs=find_params["attributes"])
        
        if "string" in find_params:
            element = soup.find(find_params["tag"], attrs=find_params["attributes"], string=find_params["string"])

        if element and "next_sibling" in self.config:
            sibling_params = self.config["next_sibling"]
            element = element.find_next_sibling(sibling_params["tag"], attrs=sibling_params["attributes"])

        if not element:
            raise ValueError(f"Price not found for {self.source_name}")
        
        price_text = element.contents[self.config['content_index']].strip() if 'content_index' in self.config else element.get_text(strip=True)
        
        return float(price_text) if self.config.get("transform") == "float" else price_text

    def _parse_with_javascript(self, soup):
        find_params = self.config["find_params"]
        element = soup.find(find_params["tag"], attrs=find_params["attributes"])

        if not element:
            raise ValueError(f"Price not found for {self.source_name}")

        price_text = element.contents[self.config['content_index']].strip() if 'content_index' in self.config else element.get_text(strip=True)

        return float(price_text) if self.config.get("transform") == "float" else price_text


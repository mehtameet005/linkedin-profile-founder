"""
Crawler Service - Responsible for web scraping with Playwright
"""
from typing import Dict, List
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class CrawlerService:
    """Service for crawling websites and extracting content"""

    def __init__(self):
        self.max_depth = 3
        self.timeout = 30000  # 30 seconds

    async def crawl_website(self, url: str) -> Dict[str, any]:
        """
        Crawl a website and extract relevant information

        Args:
            url: The website URL to crawl

        Returns:
            Dictionary containing extracted data
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(url, wait_until="networkidle", timeout=self.timeout)

                # Extract page content
                content = await page.content()
                soup = BeautifulSoup(content, "html.parser")

                # Extract text, headings, metadata
                data = {
                    "url": url,
                    "title": soup.title.string if soup.title else "",
                    "headings": [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])],
                    "paragraphs": [p.get_text(strip=True) for p in soup.find_all("p")],
                    "meta_description": self._get_meta_description(soup),
                    "links": self._extract_links(soup, url),
                }

                return data

            except Exception as e:
                logger.error(f"Error crawling {url}: {str(e)}")
                raise
            finally:
                await browser.close()

    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description from page"""
        meta = soup.find("meta", attrs={"name": "description"})
        return meta.get("content", "") if meta else ""

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract internal links from page"""
        links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/") or base_url in href:
                links.append(href)
        return links[:20]  # Limit to 20 links


# Singleton instance
crawler_service = CrawlerService()

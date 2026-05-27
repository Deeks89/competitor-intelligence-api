from firecrawl import FirecrawlApp
from app.config import settings

app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)

async def scrape_competitor_website(url: str) -> str:
    try:
        result = app.scrape_url(
            url,
            params={"formats": ["markdown"], "timeout": 30000}
        )
        if isinstance(result, dict):
            return result.get("markdown", "") or result.get("data", {}).get("markdown", "")
        return result.markdown or ""
    except Exception as e:
        print(f"Firecrawl scrape failed for {url}: {e}")
        return ""  # Return empty string — Claude will use training knowledge instead

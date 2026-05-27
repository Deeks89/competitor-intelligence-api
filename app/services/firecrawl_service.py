from firecrawl import FirecrawlApp
from app.config import settings

app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)

async def scrape_competitor_website(url: str) -> str:
    result = app.scrape_url(
        url,
        params={"formats": ["markdown"]}
    )
    if isinstance(result, dict):
        return result.get("markdown", "") or result.get("data", {}).get("markdown", "")
    return result.markdown or ""

async def scrape_g2_page(company_name: str) -> str:
    slug = company_name.lower().replace(" ", "-")
    # Use product listing page instead of /reviews — less bot protection, has ratings
    g2_url = f"https://www.g2.com/products/{slug}/"
    result = app.scrape_url(
        g2_url,
        params={"formats": ["markdown"]}
    )
    if isinstance(result, dict):
        return result.get("markdown", "") or result.get("data", {}).get("markdown", "")
    return result.markdown or ""

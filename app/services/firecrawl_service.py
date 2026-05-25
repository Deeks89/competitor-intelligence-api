# services/firecrawl_service.py — All Firecrawl scraping logic lives here
# Firecrawl handles JavaScript-rendered pages that normal scrapers can't read
# It returns clean markdown text, which is easy for Claude to process

from firecrawl import FirecrawlApp

from app.config import settings

# Create one Firecrawl client to reuse
app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)


async def scrape_competitor_website(url: str) -> str:
    """
    Scrape a competitor's website and return clean markdown text.
    Firecrawl renders the page (including JavaScript) then strips HTML,
    leaving just the readable content.
    """

    result = app.scrape_url(
        url,
        params={
            "formats": ["markdown"],  # Return content as markdown (cleaner for Claude)
        }
    )

    # The markdown content is in result.markdown
    return result.markdown or ""


async def scrape_g2_page(company_name: str) -> str:
    """
    Scrape the G2 reviews page for a given company.
    G2 is a software review site — it has ratings, review counts, and user feedback.
    """

    # Build the G2 URL for this company
    # G2 slugifies company names: "Stripe" → "stripe", "HubSpot CRM" → "hubspot-crm"
    slug = company_name.lower().replace(" ", "-")
    g2_url = f"https://www.g2.com/products/{slug}/reviews"

    result = app.scrape_url(
        g2_url,
        params={"formats": ["markdown"]}
    )

    return result.markdown or ""

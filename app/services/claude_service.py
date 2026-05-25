# services/claude_service.py — All interactions with the Claude AI API live here
# Claude does two things in this pipeline:
#   1. Discovers who the competitors are
#   2. Extracts structured signals from scraped pages

import json
import anthropic

from app.config import settings

# Create one Anthropic client to reuse across all calls
client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


async def discover_competitors(company_name: str, industry: str) -> list[dict]:
    """
    Ask Claude to identify the top competitors for a given company + industry.
    Returns a list of dicts like: [{"name": "Stripe", "website": "https://stripe.com"}, ...]
    """

    prompt = f"""You are a competitive intelligence analyst.

The user is researching: "{company_name}" in the "{industry}" industry.

Identify the top 5 direct competitors. For each competitor return ONLY a JSON array with no explanation.

Format:
[
  {{"name": "Company Name", "website": "https://companywebsite.com", "description": "One sentence about what they do"}},
  ...
]

Return only valid JSON. No markdown, no explanation."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse Claude's response text as JSON
    response_text = message.content[0].text
    competitors = json.loads(response_text)
    return competitors


async def extract_signals(scraped_content: str, competitor_name: str) -> dict:
    """
    Given raw scraped text from a competitor's website, ask Claude to extract
    structured intelligence: pricing, features, strengths, weaknesses, target market.
    Returns a dict with all extracted signals.
    """

    prompt = f"""You are a competitive intelligence analyst. Analyze the following scraped content 
from {competitor_name}'s website and extract structured intelligence.

SCRAPED CONTENT:
{scraped_content[:8000]}  

Return ONLY a JSON object (no explanation, no markdown) with this exact structure:
{{
  "pricing_model": "freemium|per-seat|flat-rate|usage-based|unknown",
  "pricing_min": 0.0,
  "pricing_max": 0.0,
  "features": ["feature 1", "feature 2", "feature 3"],
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "target_market": "Description of who this product targets"
}}

If you cannot find pricing information, use 0.0 for min/max. Return only valid JSON."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    signals = json.loads(response_text)
    return signals

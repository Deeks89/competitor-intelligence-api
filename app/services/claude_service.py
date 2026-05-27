import json
import anthropic
from app.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

async def discover_competitors(company_name: str, industry: str) -> list[dict]:
    prompt = f"""You are a competitive intelligence analyst.

The user is researching: "{company_name}" in the "{industry}" industry.

Identify the top 5 direct competitors. Return ONLY a JSON array with no explanation.

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
    response_text = message.content[0].text
    competitors = json.loads(response_text)
    return competitors


async def extract_signals(scraped_content: str, competitor_name: str) -> dict:
    prompt = f"""You are a competitive intelligence analyst. Analyze the following scraped content 
from {competitor_name}'s website and extract structured intelligence.

Also use your training knowledge about {competitor_name} to fill in any gaps — especially:
- G2 rating (a number between 1.0 and 5.0, e.g. 4.5)
- G2 review count (approximate number of reviews on G2)
- Pricing information

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
  "target_market": "Description of who this product targets",
  "g2_rating": 4.5,
  "g2_review_count": 1000
}}

Use your knowledge of {competitor_name}'s G2 presence to provide accurate rating and review count.
If you truly don't know, use null for those fields.
Return only valid JSON."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    response_text = message.content[0].text
    signals = json.loads(response_text)
    return signals

# utils/text.py — Small helper functions for cleaning and formatting text


def truncate(text: str, max_length: int = 8000) -> str:
    """Truncate text to a max length to avoid hitting API token limits."""
    if not text:
        return ""
    return text[:max_length]


def clean_scraped_text(text: str) -> str:
    """Remove excessive whitespace from scraped content."""
    if not text:
        return ""
    # Replace multiple newlines with a single one
    import re
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def slugify(name: str) -> str:
    """Convert a company name to a URL-friendly slug. e.g. 'HubSpot CRM' → 'hubspot-crm'"""
    return name.lower().strip().replace(" ", "-")

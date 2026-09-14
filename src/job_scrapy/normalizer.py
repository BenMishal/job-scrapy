import re
from datetime import datetime


def normalize_title(title: str) -> str:
    """Normalize a job title for deduplication and comparison."""
    if not title:
        return ""
    # Lowercase and strip extra whitespace
    title = title.lower().strip()
    # Remove common fluff
    title = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title) # Remove text in brackets
    title = re.sub(r'[^a-z0-9\s]', '', title) # Remove special characters
    return " ".join(title.split())

def normalize_company(company: str) -> str:
    """Normalize a company name."""
    if not company:
        return ""
    company = company.lower().strip()
    # Remove legal suffixes
    company = re.sub(r'\b(inc|llc|ltd|limited|corp|corporation)\b\.?', '', company)
    return " ".join(company.split())

def is_remote_location(location: str) -> bool:
    """Determine if a location string implies remote work."""
    if not location:
        return False
    loc = location.lower()
    return any(keyword in loc for keyword in ['remote', 'wfh', 'work from home', 'anywhere'])

def normalize_timestamp(timestamp_str: str) -> datetime | None:
    """Attempt to parse various timestamp formats into a datetime object."""
    if not timestamp_str:
        return None
        
    # Example formats to try (can be expanded based on sources)
    formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
            
    return None

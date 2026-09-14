from .models import Job
from .normalizer import normalize_company, normalize_title


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    """
    Remove duplicate jobs based on URL or normalized composite key.
    
    Hierarchy:
    1. Exact URL match (if present)
    2. Normalized Company + Normalized Title + Location
    """
    seen_urls: set[str] = set()
    seen_composite: set[str] = set()
    unique_jobs: list[Job] = []
    
    for job in jobs:
        # 1. URL Deduplication
        if job.url:
            if job.url in seen_urls:
                continue
            seen_urls.add(job.url)
            
        # 2. Composite Deduplication
        norm_title = normalize_title(job.title)
        norm_company = normalize_company(job.company)
        norm_location = job.location.lower().strip() if job.location else "unknown"
        
        composite_key = f"{norm_company}::{norm_title}::{norm_location}"
        
        if composite_key in seen_composite:
            continue
            
        seen_composite.add(composite_key)
        unique_jobs.append(job)
        
    return unique_jobs

import concurrent.futures
import logging

from ..config import settings
from ..deduplicator import deduplicate_jobs
from ..models import Job
from ..sources.jobspy_source import JobspySource
from ..sources.remote_api_sources import RemoteAPISource

logger = logging.getLogger(__name__)

def search_all_jobs(
    query: str,
    location: str = "Remote",
    country: str | None = None,
    hours_old: int = 168,
    remote: bool = False,
    results_limit: int = 50,
    sources_to_use: list[str] | None = None
) -> list[Job]:
    """
    Orchestrates the search across multiple job sources and deduplicates results.
    """
    search_terms = [query] if query else []
    
    # Initialize sources
    available_sources = {
        "jobspy": JobspySource(),
        "remote_api": RemoteAPISource()
    }
    
    active_sources = []
    if sources_to_use:
        for s in sources_to_use:
            if s.lower() in available_sources:
                active_sources.append(available_sources[s.lower()])
    else:
        active_sources = list(available_sources.values())
        
    all_jobs: list[Job] = []
    
    logger.info(f"Executing search for '{query}' across {len(active_sources)} sources.")

    # Execute searches concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings.max_concurrency) as executor:
        future_to_source = {
            executor.submit(
                source.search_jobs, 
                search_terms=search_terms, 
                location=location,
                country=country,
                hours_old=hours_old
            ): source.__class__.__name__ for source in active_sources
        }
        
        for future in concurrent.futures.as_completed(future_to_source):
            source_name = future_to_source[future]
            try:
                jobs = future.result()
                logger.info(f"Source {source_name} returned {len(jobs)} jobs.")
                all_jobs.extend(jobs)
            except Exception as e:
                logger.error(f"Source {source_name} generated an exception: {e}")
                
    # Filter for remote if requested
    if remote:
        all_jobs = [j for j in all_jobs if j.remote]
        
    # Deduplicate
    unique_jobs = deduplicate_jobs(all_jobs)
    logger.info(f"Total jobs after deduplication: {len(unique_jobs)}")
    
    # Sort and limit
    # We could sort by date posted if we had reliable timestamps, but for now we'll just limit
    return unique_jobs[:results_limit]

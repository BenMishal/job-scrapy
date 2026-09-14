import logging

import pandas as pd
from jobspy import scrape_jobs

from ..config import settings
from ..models import Job
from ..normalizer import is_remote_location
from .base import JobSource

logger = logging.getLogger(__name__)

class JobspySource(JobSource):
    """Scrapes jobs using the JobSpy library (LinkedIn, Indeed, Glassdoor, ZipRecruiter)."""
    
    def search_jobs(self, search_terms: list[str], location: str = "Remote", **kwargs) -> list[Job]:
        logger.info(f"Starting JobSpy search for {search_terms} in {location}")
        
        country = kwargs.get("country", None)
        hours_old = kwargs.get("hours_old", 168)  # Default 7 days
        
        all_jobs: list[Job] = []
        
        for term in search_terms:
            logger.debug(f"JobSpy scraping term: {term}")
            try:
                # jobspy arguments
                scrape_kwargs = {
                    "site_name": ["linkedin", "indeed", "glassdoor", "zip_recruiter"],
                    "search_term": term,
                    "location": location,
                    "results_wanted": settings.max_results,
                    "hours_old": hours_old,
                    "linkedin_fetch_description": True
                }
                
                if country:
                    scrape_kwargs["country_indeed"] = country
                    
                # Note: If proxy settings were needed, they would go here.
                # E.g. scrape_kwargs["proxies"] = [...]
                
                # We do NOT implement anti-bot evasion beyond what jobspy does inherently.
                jobs_df = scrape_jobs(**scrape_kwargs)
                
                if isinstance(jobs_df, pd.DataFrame) and not jobs_df.empty:
                    for _, row in jobs_df.iterrows():
                        # JobSpy returns specific column names
                        try:
                            job = Job(
                                title=str(row.get("title", "")),
                                company=str(row.get("company", "")),
                                location=str(row.get("location", location)),
                                url=str(row.get("job_url", "")),
                                source=str(row.get("site", "jobspy")),
                                description=str(row.get("description", "")),
                                remote=is_remote_location(str(row.get("location", location))) or row.get("is_remote", False)
                            )
                            all_jobs.append(job)
                        except Exception as parse_e:
                            logger.warning(f"Failed to parse job from JobSpy row: {parse_e}")
                            
            except Exception as e:
                logger.error(f"JobSpy failed for term '{term}': {e}")
                
        return all_jobs

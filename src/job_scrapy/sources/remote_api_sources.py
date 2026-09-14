import logging

import requests

from ..config import settings
from ..models import Job
from .base import JobSource

logger = logging.getLogger(__name__)

class RemoteAPISource(JobSource):
    """Scrapes jobs from various open remote job APIs (Remotive, RemoteOK, Himalayas, Arbeitnow)."""
    
    def search_jobs(self, search_terms: list[str], location: str = "Remote", **kwargs) -> list[Job]:
        logger.info(f"Starting Remote APIs search for {search_terms}")
        all_jobs: list[Job] = []
        
        # Helper to check if title matches any search term
        def is_relevant(title: str) -> bool:
            if not search_terms:
                return True
            title_lower = title.lower()
            return any(term.lower() in title_lower for term in search_terms)

        # 1. Remotive
        try:
            res = requests.get('https://remotive.com/api/remote-jobs?category=data', timeout=settings.timeout)
            if res.ok:
                for j in res.json().get('jobs', []):
                    if is_relevant(j.get('title', '')):
                        all_jobs.append(Job(
                            title=j.get('title', ''),
                            company=j.get('company_name', ''),
                            location=j.get('candidate_required_location', 'Remote'),
                            url=j.get('url', ''),
                            source='Remotive',
                            description=j.get('description', ''),
                            remote=True
                        ))
        except Exception as e:
            logger.error(f"Remotive API failed: {e}")

        # 2. Arbeitnow
        try:
            res = requests.get('https://www.arbeitnow.com/api/job-board-api', timeout=settings.timeout)
            if res.ok:
                for j in res.json().get('data', []):
                    if is_relevant(j.get('title', '')):
                        all_jobs.append(Job(
                            title=j.get('title', ''),
                            company=j.get('company_name', ''),
                            location=j.get('location', 'Remote'),
                            url=j.get('url', ''),
                            source='Arbeitnow',
                            description=j.get('description', ''),
                            remote=True
                        ))
        except Exception as e:
            logger.error(f"Arbeitnow API failed: {e}")
            
        # 3. Himalayas
        try:
            res = requests.get('https://himalayas.app/jobs/api', timeout=settings.timeout)
            if res.ok:
                for j in res.json().get('jobs', []):
                    if is_relevant(j.get('title', '')):
                        locs = j.get('locationRestrictions', [])
                        loc_str = ", ".join(locs) if isinstance(locs, list) else str(locs)
                        all_jobs.append(Job(
                            title=j.get('title', ''),
                            company=j.get('companyName', ''),
                            location=loc_str or 'Remote',
                            url=j.get('jobUrl', j.get('applicationLink', '')),
                            source='Himalayas',
                            description=j.get('description', ''),
                            remote=True
                        ))
        except Exception as e:
            logger.error(f"Himalayas API failed: {e}")
            
        # Note: We omit APIs that require keys if they aren't provided to avoid logging errors needlessly
        # If API keys are available, we can add Findwork, Jooble, etc. here as well.
        
        return all_jobs

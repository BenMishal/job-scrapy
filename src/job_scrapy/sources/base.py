from typing import Protocol

from ..models import Job


class JobSource(Protocol):
    """Protocol that all job sources must implement."""
    
    def search_jobs(self, search_terms: list[str], location: str = "Remote", **kwargs) -> list[Job]:
        """
        Search the specific job source for the given terms.
        
        Args:
            search_terms: A list of keywords or titles to search for.
            location: The location to search in.
            **kwargs: Additional parameters (e.g., country, hours_old).
            
        Returns:
            A list of validated Job models.
        """
        ...

import logging

from mcp.server.fastmcp import FastMCP

# Configure logging before importing local modules
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from src.job_scrapy.services.search import search_all_jobs

# Create a FastMCP server
mcp = FastMCP("Job Scraper")

@mcp.tool()
def search_jobs(
    query: str, 
    location: str = "Remote", 
    country: str | None = None,
    hours_old: int = 168,
    remote: bool = False,
    results_limit: int = 20,
    sources: list[str] | None = None
) -> str:
    """
    Search for jobs across multiple job sources including LinkedIn, Indeed, Glassdoor, and remote API boards.
    
    Args:
        query: Job title or keywords (e.g., "Business Analyst", "Python Developer").
        location: City, State, or "Remote". Defaults to "Remote".
        country: Optional country parameter for accurate localization (e.g., "UAE", "India").
        hours_old: Filter jobs posted in the last X hours (default 168 = 7 days).
        remote: If true, filters for strictly remote jobs.
        results_limit: Maximum number of jobs to return.
        sources: Optional list of sources to restrict search (e.g., ["jobspy", "remote_api"]).
    """
    try:
        jobs = search_all_jobs(
            query=query,
            location=location,
            country=country,
            hours_old=hours_old,
            remote=remote,
            results_limit=results_limit,
            sources_to_use=sources
        )
        
        if not jobs:
            return f"No jobs found for '{query}' in '{location}'."
            
        result = []
        for job in jobs:
            # Format nicely for markdown
            # Format nicely for markdown
            md = f"### {job.title} at {job.company}\n"
            md += f"- **Location**: {job.location}\n"
            md += f"- **Source**: {job.source}\n"
            if job.url:
                md += f"- **URL**: {job.url}\n"
            result.append(md)
            
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"An error occurred during search: {e!s}"

@mcp.tool()
def search_remote_jobs(query: str, results_limit: int = 20) -> str:
    """
    Specifically search for strictly remote jobs across all available remote APIs.
    
    Args:
        query: Job title or keywords (e.g., "Data Analyst").
        results_limit: Maximum number of jobs to return.
    """
    return search_jobs(query=query, location="Remote", remote=True, results_limit=results_limit, sources=["remote_api"])

@mcp.tool()
def list_available_sources() -> str:
    """List the job boards currently supported by Job Scrapy."""
    sources = [
        "- **JobSpy**: Scrapes LinkedIn, Indeed, Glassdoor, and ZipRecruiter.",
        "- **Remote APIs**: Scrapes Remotive, Arbeitnow, Himalayas, and RemoteOK."
    ]
    return "\n".join(sources)

if __name__ == "__main__":
    # Run the server using stdio transport (compatible with Claude, Antigravity, etc.)
    mcp.run(transport='stdio')

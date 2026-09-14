from mcp.server.fastmcp import FastMCP
from typing import List, Optional
import pandas as pd
import json

from sources.jobspy_source import collect_jobspy_jobs
from sources.remote_api_source import collect_remote_api_jobs

# Create a FastMCP server
mcp = FastMCP("Job Scraper")

def format_jobs(df: pd.DataFrame) -> str:
    """Format the dataframe of jobs into a markdown string."""
    if df.empty:
        return "No jobs found for this query."
        
    result = []
    # Limit to top 20 to avoid exceeding context windows
    for index, row in df.head(20).iterrows():
        title = row.get("job_title", "Unknown Title")
        company = row.get("company", "Unknown Company")
        location = row.get("location", "Unknown Location")
        site = row.get("site", row.get("source_query", "Unknown Source"))
        url = row.get("job_url", "")
        
        job_md = f"### {title} at {company}\n"
        job_md += f"- **Location**: {location}\n"
        job_md += f"- **Source**: {site}\n"
        if url:
            job_md += f"- **URL**: {url}\n"
            
        result.append(job_md)
        
    if len(df) > 20:
        result.append(f"\n*...and {len(df) - 20} more jobs not shown to save space.*")
        
    return "\n".join(result)

@mcp.tool()
def search_jobspy(search_terms: List[str], locations: List[str], country: Optional[str] = None) -> str:
    """
    Scrape job boards (LinkedIn, Indeed, Glassdoor, ZipRecruiter) for specific roles.
    
    Args:
        search_terms: List of job titles to search for (e.g., ["business analyst", "data analyst"])
        locations: List of locations to search in (e.g., ["Dubai", "London"])
        country: Optional country parameter for Indeed localization (e.g., "India", "UAE")
    """
    try:
        def log_callback(msg):
            pass # Suppress logs so they don't break stdout communication
            
        df = collect_jobspy_jobs(search_terms, locations, country, log_callback=log_callback)
        return format_jobs(df)
    except Exception as e:
        return f"Error scraping JobSpy: {str(e)}"

@mcp.tool()
def search_remote_apis(search_terms: List[str]) -> str:
    """
    Scrape remote-focused job boards (Remotive, RemoteOK, Himalayas, etc.) for specific roles.
    
    Args:
        search_terms: List of keywords/job titles to search for (e.g., ["data analyst"])
    """
    try:
        def log_callback(msg):
            pass # Suppress logs
            
        df = collect_remote_api_jobs(search_terms, log_callback=log_callback)
        return format_jobs(df)
    except Exception as e:
        return f"Error scraping Remote APIs: {str(e)}"

if __name__ == "__main__":
    # Run the server using stdio transport (compatible with Claude, Antigravity, etc.)
    mcp.run(transport='stdio')

from datetime import datetime

from pydantic import BaseModel, Field


class Job(BaseModel):
    """Standardized Job Model representing a normalized job posting."""
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(default="Remote", description="Job location (City, State, or 'Remote')")
    country: str | None = Field(default=None, description="Country of the job")
    city: str | None = Field(default=None, description="City of the job")
    
    description: str | None = Field(default=None, description="Full job description")
    url: str | None = Field(default=None, description="URL to the job posting")
    
    source: str = Field(..., description="The platform the job was scraped from (e.g., LinkedIn, RemoteOK)")
    source_id: str | None = Field(default=None, description="The unique ID of the job on the source platform")
    
    posted_at: datetime | None = Field(default=None, description="When the job was posted (ISO-8601)")
    scraped_at: datetime = Field(default_factory=datetime.utcnow, description="When the job was scraped (ISO-8601)")
    
    salary_min: float | None = Field(default=None, description="Minimum salary")
    salary_max: float | None = Field(default=None, description="Maximum salary")
    salary_currency: str | None = Field(default=None, description="Salary currency (e.g., USD)")
    
    remote: bool = Field(default=False, description="Is the job remote?")
    employment_type: str | None = Field(default=None, description="E.g., Full-time, Part-time, Contract")
    job_type: str | None = Field(default=None, description="Job category or domain")
    
    skills: list[str] = Field(default_factory=list, description="Extracted skills")
    company_url: str | None = Field(default=None, description="URL to the company website or profile")

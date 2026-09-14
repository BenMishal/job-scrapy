import pytest

from src.job_scrapy.models import Job


def test_job_model_creation():
    job = Job(
        title="Software Engineer",
        company="Tech Corp",
        location="Remote",
        source="LinkedIn"
    )
    assert job.title == "Software Engineer"
    assert job.company == "Tech Corp"
    assert job.remote is False  # By default, based on our setup it relies on the boolean flag

def test_job_model_missing_required():
    with pytest.raises(ValueError):
        Job(company="Tech Corp", source="LinkedIn")

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# ==========================================
# SEARCH PARAMETERS
# ==========================================
SEARCH_TERMS = [
    "business analyst",
    "business data analyst",
    "product analyst",
    "operations analyst",
    "growth analyst",
    "strategy analyst",
    "customer insights analyst",
    "crm analyst",
    "business operations",
    "founder’s office"
]

REGION_LOCATIONS = {
    "India": ["Bengaluru", "Chennai", "Hyderabad", "Pune", "Gurgaon", "India"],
    "UK": ["London", "Manchester", "Birmingham", "United Kingdom"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Canada"],
    "Gulf": ["Dubai", "Abu Dhabi", "Bahrain", "Riyadh", "UAE"],
    "USA": ["New York", "San Francisco", "Austin", "United States"]
}

INTERNATIONAL_SEARCH_TERMS = [
    "business analyst visa sponsorship",
    "data analyst visa sponsorship",
    "product analyst visa sponsorship",
    "business analyst relocation",
    "data analyst relocation support",
    "tier 2 sponsorship analyst"
]

MAX_JOB_AGE_DAYS = 7 # Roughly 168 hours
RESULTS_WANTED_PER_QUERY = 20 # Adjust as needed to avoid rate limits

# ==========================================
# FILTERING KEYWORDS
# ==========================================
# Roles that match these will be given a small negative penalty, but not outright removed.
SOFT_EXCLUDE_KEYWORDS = [
    "senior", "lead", "manager", "director", "head",
    "software engineer"
]
# Remote API Settings
REMOTIVE_LIMIT = 50

# Proxy Settings (Loaded from proxies.txt if it exists)
# JOBSPY_PROXIES = []
# proxy_file = os.path.join(os.path.dirname(__file__), "proxies.txt")
# if os.path.exists(proxy_file):
#     with open(proxy_file, "r") as f:
#         JOBSPY_PROXIES = [line.strip() for line in f if line.strip()]
JOBSPY_PROXIES = None

# Pipeline Configuration
# Roles that match these will be removed entirely
EXCLUDE_KEYWORDS = [
    "software engineer",
    "full stack",
    "java developer",
    "data engineer",
    "ml engineer",
    "machine learning engineer",
    "devops",
    "qa ",
    "sales executive",
    "business development executive", # mostly sales
]

# Jobs must have at least one of these signals to pass filtering
TARGET_KEYWORDS = [
    "sql",
    "power bi",
    "excel",
    "dashboard",
    "kpi",
    "analytics",
    "reporting",
    "operations",
    "customer insights",
    "business intelligence"
]

# ==========================================
# SCORING PARAMETERS
# ==========================================
TOP_CITIES = [city for region in REGION_LOCATIONS.values() for city in region]
REMOTE_KEYWORDS = ["remote", "work from home", "wfh"]
STARTUP_KEYWORDS = ["startup", "saas", "edtech", "d2c", "healthcare", "hospitality", "consulting"]
BONUS_KEYWORDS = ["stakeholder", "cross-functional", "growth", "business insights"]

SCORING_WEIGHTS = {
    "title_strong_match": 20,
    "sql_mentioned": 15,
    "power_bi_mentioned": 12,
    "excel_mentioned": 10,
    "analytics_keywords": 10,
    "top_city": 8,
    "remote": 8,
    "startup_keywords": 6,
    "experience_0_2_years": 8,  # (Legacy, still useful for text scoring)
    "experience_3_years": 5,    # (Legacy, still useful for text scoring)
    "experience_perfect_match": 10, # Bonus for strictly meeting 0-3 exp requirement
    "salary_meets_target": 10,
    "salary_exceeds_target": 15,
    "salary_missing": 0,
    "salary_low": -10,
    "too_technical": -15,
    "too_senior": -10,
    "mostly_sales": -8,
    "bonus_keywords": 5
}

# ==========================================
# EXTRACTION & FILTERING LIMITS
# ==========================================
MAX_EXPERIENCE_YEARS = 3
TARGET_SALARY_LPA_MIN = 6.0
TARGET_SALARY_LPA_MAX = 75.0
ENABLE_LOCAL_AI_RERANKING = False # Placeholder for future free AI layer

# ==========================================
# SYSTEM / RUN CONFIGURATION
# ==========================================
ENABLE_JOBSPY = True
ENABLE_APIFY = False
ENABLE_MANUAL_IMPORT = True

# Read Apify token if it exists (for dynamic runs)
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
APIFY_NAUKRI_ACTOR_ID = os.getenv("APIFY_NAUKRI_ACTOR_ID", "") # E.g., generic actor ID if you have one
# If ENABLE_APIFY is True but the above are empty, it will try to read from a local apify_results.json/csv

# ------------------------------------------
# API KEYS
# ------------------------------------------
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# --- NEW SECURED APIS ---
FINDWORK_API_KEY = os.getenv("FINDWORK_API_KEY", "eaa1a6e379f8f65cf6f5939f1ec8917aed0de819")
JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY", "fa0ff009-555d-4feb-91f4-781da82f7b32")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "7e9abb1f")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "10b6be26e1d44d74b878b64a93cfd7a6")
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "GEYkS0vs1fRXwaqZ/cuqImmB3NmbiPUvkeJq08au2z8=")
THEMUSE_API_KEY = os.getenv("THEMUSE_API_KEY", "80f753bf2f5e88a3faf4bc90122df4d1ef548660e2bb3ac841f640e5acd2f915")

MAX_SERPAPI_QUERIES_PER_RUN = 10
SERPAPI_HIGH_VALUE_QUERIES = [
    "Data Analyst visa sponsorship UAE 0 to 3 years experience",
    "Junior Business Analyst UAE visa sponsorship",
    "Product Analyst visa sponsorship UAE",
    "Data Analyst visa sponsorship Dubai",
    "Operations Analyst visa sponsorship UAE",
    "Growth Analyst visa sponsorship UAE",
    "Strategy Analyst visa sponsorship Dubai",
    "Data Scientist visa sponsorship UAE 0 to 3 years",
    "Business Intelligence Analyst visa sponsorship UAE",
    "Entry level data analyst sponsorship Dubai"
]

OUTPUT_FOLDER = "output"
RAW_FILE = f"{OUTPUT_FOLDER}/raw_jobs.csv"
FILTERED_FILE = f"{OUTPUT_FOLDER}/filtered_jobs.csv"
PRIORITIZED_FILE = f"{OUTPUT_FOLDER}/prioritized_jobs.csv"
SHORTLIST_FILE = f"{OUTPUT_FOLDER}/shortlist_jobs.csv"
SEEN_JOBS_FILE = f"{OUTPUT_FOLDER}/seen_jobs.csv"
MASTER_HISTORY_FILE = f"{OUTPUT_FOLDER}/master_history.csv"

INTL_RAW_FILE = f"{OUTPUT_FOLDER}/intl_raw_jobs.csv"
INTL_FILTERED_FILE = f"{OUTPUT_FOLDER}/intl_filtered_jobs.csv"
INTL_PRIORITIZED_FILE = f"{OUTPUT_FOLDER}/intl_prioritized_jobs.csv"
INTL_SHORTLIST_FILE = f"{OUTPUT_FOLDER}/intl_shortlist_jobs.csv"

LOCAL_APIFY_RESULTS = f"apify_results.json"
MANUAL_IMPORT_FILE = "manual_jobs.csv"

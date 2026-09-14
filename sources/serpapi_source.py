import pandas as pd
import requests
import datetime
import config

def collect_serpapi_jobs(search_terms=None, check_stop=lambda: False, log_callback=print):
    """
    Fetches jobs using SerpApi's Google Jobs engine.
    Strictly rate-limited to avoid exhausting the free tier.
    """
    if not config.SERPAPI_KEY:
        log_callback("SERPAPI_KEY not found in environment. Skipping SerpApi Google Jobs.")
        return pd.DataFrame()
        
    log_callback("Starting SerpApi Google Jobs collection...")
    all_jobs = []
    
    # Search terms come from the uploaded CV when available. The previous fixed
    # analyst-only queries remain only as a fallback for runs without a CV.
    queries = (search_terms or config.SERPAPI_HIGH_VALUE_QUERIES)[:config.MAX_SERPAPI_QUERIES_PER_RUN]
    
    for i, query in enumerate(queries):
        if check_stop():
            break
            
        log_callback(f"[{i+1}/{len(queries)}] SerpApi querying: '{query}'")
        
        # To save budget, we will only fetch page 1 (10 jobs) per query.
        # If we wanted page 2, we would increment 'start' parameter by 10 and burn another credit.
        params = {
            "engine": "google_jobs",
            "q": query,
            "hl": "en",
            "api_key": config.SERPAPI_KEY,
            "start": 0
        }
        
        try:
            res = requests.get("https://serpapi.com/search.json", params=params, timeout=20)
            if res.ok:
                data = res.json()
                jobs_results = data.get("jobs_results", [])
                
                log_callback(f"    -> Found {len(jobs_results)} jobs for this query.")
                
                for j in jobs_results:
                    # Parse SerpApi's structure into our common dataframe structure
                    title = j.get("title", "")
                    company = j.get("company_name", "")
                    location = j.get("location", "")
                    description = j.get("description", "")
                    
                    # Some jobs have an array of apply links
                    apply_links = j.get("apply_options", [])
                    job_url = apply_links[0].get("link", "") if apply_links else ""
                    
                    # Sometimes there is no clear date, but we can store 'Recent'
                    all_jobs.append({
                        'job_title': title,
                        'company': company,
                        'location': location,
                        'description': description,
                        'job_url': job_url,
                        'date_posted': "Recent",
                        'site': "Google Jobs",
                        'source_query': f"serpapi: {query}"
                    })
            else:
                log_callback(f"    -> SerpApi error: {res.status_code} {res.text}")
        except Exception as e:
            log_callback(f"    -> Error connecting to SerpApi: {e}")
            
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        log_callback(f"Total SerpApi Jobs fetched: {len(df)}")
        return df
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    df = collect_serpapi_jobs()
    print(df.head())
    print(f"Total: {len(df)}")

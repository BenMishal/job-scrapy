import pandas as pd
from jobspy import scrape_jobs
import concurrent.futures
import config

def collect_jobspy_jobs(search_terms, locations, country=None, check_stop=lambda: False, log_callback=print):
    log_callback("Starting JobSpy collection...")
    all_jobs_dfs = []
    
    # Calculate hours old
    hours_old = config.MAX_JOB_AGE_DAYS * 24

    total_queries = len(search_terms) * len(locations)
    query_count = 0

    for term in search_terms:
        for loc in locations:
            if check_stop():
                log_callback("Scraping stopped by user.")
                break
                
            query_count += 1
            log_callback(f"[{query_count}/{total_queries}] Scraping JobSpy for '{term}' in '{loc}'...")
            
            try:
                kwargs = {
                    "site_name": ["linkedin", "indeed", "glassdoor", "zip_recruiter"],
                    "search_term": term,
                    "location": loc,
                    "results_wanted": config.RESULTS_WANTED_PER_QUERY,
                    "hours_old": hours_old,
                    "linkedin_fetch_description": True
                }
                
                if country:
                    kwargs["country_indeed"] = country
                    
                if getattr(config, "JOBSPY_PROXIES", None):
                    kwargs["proxies"] = config.JOBSPY_PROXIES
                    
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(scrape_jobs, **kwargs)
                    try:
                        # 3-minute hard timeout per query to prevent proxy deadlocks
                        jobs = future.result(timeout=180)
                    except concurrent.futures.TimeoutError:
                        log_callback(f"    -> Timeout Error: JobSpy hanging. Skipping.")
                        continue
                
                if isinstance(jobs, pd.DataFrame) and not jobs.empty:
                    # Add source query
                    jobs['source_query'] = f"jobspy: {term} in {loc}"
                    all_jobs_dfs.append(jobs)
                    log_callback(f"    -> Found {len(jobs)} jobs.")
                else:
                    log_callback("    -> No jobs found.")
            except Exception as e:
                log_callback(f"    -> Error scraping {term} in {loc}: {e}")
                
        if check_stop():
            break
                
    if all_jobs_dfs:
        combined_df = pd.concat(all_jobs_dfs, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # Test script standalone
    df = collect_jobspy_jobs(config.SEARCH_TERMS, config.LOCATIONS, 'India')
    print(df.head())

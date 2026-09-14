import os
import json
import pandas as pd
from apify_client import ApifyClient
import config

def collect_apify_jobs():
    print("Checking for Apify Naukri jobs...")
    
    jobs_data = []

    # 1. Try to read from Apify API if configured
    if config.APIFY_API_TOKEN and config.APIFY_NAUKRI_ACTOR_ID:
        print("  -> Apify API credentials found. Attempting to run Actor (this may take a while)...")
        try:
            client = ApifyClient(config.APIFY_API_TOKEN)
            
            # Prepare generic run inputs for Naukri (you may need to adapt these keys to your specific actor)
            run_input = {
                "searchKeywords": config.SEARCH_TERMS[0], # Just using the first as an example for dynamic run
                "locations": config.LOCATIONS[0],
                "maxItems": config.RESULTS_WANTED_PER_QUERY
            }
            
            # Start the actor and wait for it to finish
            run = client.actor(config.APIFY_NAUKRI_ACTOR_ID).call(run_input=run_input)
            
            # Fetch and print actor results from the run's dataset
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                jobs_data.append(item)
            
            print(f"  -> Collected {len(jobs_data)} jobs via API.")
        except Exception as e:
            print(f"  -> Error running Apify Actor: {e}")
            
    # 2. If no API data was fetched, look for a local JSON or CSV
    if not jobs_data:
        if os.path.exists(config.LOCAL_APIFY_RESULTS):
            print(f"  -> Loading local Apify results from {config.LOCAL_APIFY_RESULTS}...")
            try:
                if config.LOCAL_APIFY_RESULTS.endswith('.json'):
                    with open(config.LOCAL_APIFY_RESULTS, 'r', encoding='utf-8') as f:
                        jobs_data = json.load(f)
                elif config.LOCAL_APIFY_RESULTS.endswith('.csv'):
                    df = pd.read_csv(config.LOCAL_APIFY_RESULTS)
                    jobs_data = df.to_dict('records')
                    
                print(f"  -> Loaded {len(jobs_data)} jobs locally.")
            except Exception as e:
                print(f"  -> Error loading local file: {e}")
        else:
            print(f"  -> No API run and no local '{config.LOCAL_APIFY_RESULTS}' found.")

    if not jobs_data:
        return pd.DataFrame()

    # Normalize data into standard format
    # Because different Apify Actors return different JSON structures, 
    # we make best-effort guesses for common keys.
    normalized = []
    for item in jobs_data:
        # Fallback to empty string if keys aren't found
        title = item.get('title') or item.get('jobTitle') or ''
        company = item.get('company') or item.get('companyName') or ''
        location = item.get('location') or item.get('city') or ''
        url = item.get('url') or item.get('jobUrl') or ''
        description = item.get('description') or item.get('jobDescription') or ''
        date_posted = item.get('postedAt') or item.get('date') or ''
        
        normalized.append({
            'title': title,
            'company': company,
            'location': location,
            'job_url': url,
            'description': description,
            'date_posted': date_posted,
            'source_query': 'apify: loaded'
        })
        
    df = pd.DataFrame(normalized)
    return df

if __name__ == "__main__":
    # Test script standalone
    df = collect_apify_jobs()
    print(df.head())

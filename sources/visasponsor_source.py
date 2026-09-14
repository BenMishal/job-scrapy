import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def is_relevant(title, search_terms):
    title = str(title).lower()
    fluff = {'visa', 'sponsorship', 'tier', '2', 'relocation', 'support', 'jobs', 'in', 'dubai', 'uae', 'uk', 'usa', 'canada'}
    core_keywords = {w.lower() for t in search_terms for w in t.split() if w.lower() not in fluff}
    if not core_keywords: return True
    return any(k in title for k in core_keywords)

def collect_visasponsor_jobs(search_terms, log_callback=print):
    log_callback("Starting VisaSponsor.jobs collection...")
    all_jobs = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    # We will fetch the first 3 pages of their recent jobs
    for page in range(1, 4):
        log_callback(f"    -> Fetching VisaSponsor.jobs page {page}...")
        url = f"https://visasponsor.jobs/api/jobs?page={page}"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if not res.ok:
                log_callback(f"    -> Failed to fetch page {page}: {res.status_code}")
                break
                
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', href=True)
            job_links = [l for l in links if '/api/jobs/' in l['href'] and len(l['href'].split('/')) > 3]
            
            if not job_links:
                break
                
            for a in job_links:
                job_url = "https://visasponsor.jobs" + a['href']
                
                # The text usually looks like:
                # "Data Analyst   CompanyName   London, United Kingdom   Tier 2   Publish date 11-06-2026"
                raw_text = a.text.strip().replace('\n', ' ')
                
                # Use regex to collapse multiple spaces to single
                clean_text = re.sub(r'\s{2,}', ' | ', raw_text)
                parts = clean_text.split(' | ')
                
                # Basic parsing based on observed structure
                title = parts[0] if len(parts) > 0 else "Unknown Title"
                company = parts[1] if len(parts) > 1 else "Unknown Company"
                location = parts[2] if len(parts) > 2 else "Unknown Location"
                
                # Check against user search terms
                if is_relevant(title, search_terms):
                    all_jobs.append({
                        'job_title': title,
                        'company': company,
                        'location': location,
                        'description': f"Sponsorship explicitly mentioned. Extracted from: {job_url}",
                        'job_url': job_url,
                        'date_posted': "Recent",
                        'site': "VisaSponsor.jobs",
                        'source_query': "visasponsor_scrape"
                    })
        except Exception as e:
            log_callback(f"    -> Error scraping VisaSponsor.jobs: {e}")
            break
            
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        log_callback(f"Total VisaSponsor.jobs matched: {len(df)}")
        return df
    else:
        log_callback("No VisaSponsor.jobs matched.")
        return pd.DataFrame()

if __name__ == "__main__":
    df = collect_visasponsor_jobs(["data", "analyst", "developer", "engineer"])
    print(df.head())
    print(f"Total matched: {len(df)}")

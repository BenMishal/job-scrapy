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

def collect_englishjobs_jobs(search_terms, log_callback=print):
    log_callback("Starting EnglishJobs.de collection...")
    all_jobs = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    # We will search the primary keyword 'data', 'analyst', 'product'
    # Englishjobs usually handles simple queries via /jobs/{term}
    # To be safe, we just scrape /jobs/data-analyst and /jobs/business-analyst
    
    urls_to_scrape = [
        "https://englishjobs.de/jobs/data-analyst",
        "https://englishjobs.de/jobs/business-analyst",
        "https://englishjobs.de/jobs/product-manager",
        "https://englishjobs.de/jobs/data-scientist"
    ]
    
    for url in urls_to_scrape:
        log_callback(f"    -> Fetching {url}...")
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if not res.ok:
                continue
            
            soup = BeautifulSoup(res.text, 'html.parser')
                
            job_cards = soup.find_all('li', class_=lambda c: c and 'job' in c.lower())
            if not job_cards:
                job_cards = soup.find_all('div', class_=lambda c: c and 'job' in c.lower())
            
            for card in job_cards:
                a_tag = card.find('a', href=True)
                if not a_tag or '/job/' not in a_tag['href']:
                    continue
                    
                job_url = "https://englishjobs.de" + a_tag['href']
                
                # Extract text from the whole card
                raw_text = card.text.strip().replace('\n', ' ')
                clean_text = re.sub(r'\s{2,}', ' | ', raw_text)
                
                parts = clean_text.split(' | ')
                
                if len(parts) >= 2:
                    title = parts[0]
                    company = parts[1]
                    location = parts[2] if len(parts) > 2 else "Germany"
                else:
                    title = clean_text
                    company = "Unknown"
                    location = "Germany"
                    
                # Fix specific parsing glitch where date is appended to company
                if company and len(company.split()) > 4:
                    company = company.split('  ')[0] # Usually double space separator
                    
                # Check against user search terms
                if is_relevant(title, search_terms):
                    all_jobs.append({
                        'job_title': title,
                        'company': company,
                        'location': location,
                        'description': f"English-speaking role in Germany. URL: {job_url}",
                        'job_url': job_url,
                        'date_posted': "Recent",
                        'site': "EnglishJobs.de",
                        'source_query': "englishjobs_scrape"
                    })
        except Exception as e:
            log_callback(f"    -> Error scraping EnglishJobs.de: {e}")
            
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        # Drop duplicates based on URL
        df = df.drop_duplicates(subset=['job_url'])
        log_callback(f"Total EnglishJobs.de matched: {len(df)}")
        return df
    else:
        log_callback("No EnglishJobs.de matched.")
        return pd.DataFrame()

if __name__ == "__main__":
    df = collect_englishjobs_jobs(["data", "analyst"])
    print(df.head())
    print(f"Total matched: {len(df)}")

import pandas as pd
import requests
import datetime
import config

def is_relevant(title, search_terms):
    title = str(title).lower()
    fluff = {'visa', 'sponsorship', 'tier', '2', 'relocation', 'support', 'jobs', 'in', 'dubai', 'uae', 'uk', 'usa', 'canada'}
    core_keywords = {w.lower() for t in search_terms for w in t.split() if w.lower() not in fluff}
    if not core_keywords: return True
    return any(k in title for k in core_keywords)

def collect_remote_api_jobs(search_terms, log_callback=print):
    log_callback("Starting Remote API collection (Remotive & RemoteOK)...")
    all_jobs = []
    
    # 1. Fetch from Remotive
    try:
        log_callback("Fetching from Remotive API...")
        # Remotive has a 'data' category
        res = requests.get('https://remotive.com/api/remote-jobs?category=data', timeout=15)
        if res.ok:
            jobs_data = res.json().get('jobs', [])
            log_callback(f"    -> Remotive returned {len(jobs_data)} data category jobs.")
            for j in jobs_data:
                title = str(j.get('title', '')).lower()
                # Simple keyword filter
                if is_relevant(title, search_terms):
                    all_jobs.append({
                        'job_title': j.get('title', ''),
                        'company': j.get('company_name', ''),
                        'location': j.get('candidate_required_location', 'Remote'),
                        'description': j.get('description', ''),
                        'job_url': j.get('url', ''),
                        'date_posted': j.get('publication_date', ''),
                        'site': 'Remotive',
                        'source_query': 'remotive_api'
                    })
    except Exception as e:
        log_callback(f"Error fetching from Remotive: {e}")

    # 2. Fetch from RemoteOK
    try:
        log_callback("Fetching from RemoteOK API...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get('https://remoteok.com/api', headers=headers, timeout=15)
        if res.ok:
            jobs_data = res.json()
            if len(jobs_data) > 0 and 'legal' in jobs_data[0]:
                jobs_data = jobs_data[1:] # Skip first item (legal disclaimers)
                
            log_callback(f"    -> RemoteOK returned {len(jobs_data)} total jobs.")
            for j in jobs_data:
                title = str(j.get('position', '')).lower()
                if is_relevant(title, search_terms):
                    all_jobs.append({
                        'job_title': j.get('position', ''),
                        'company': j.get('company', ''),
                        'location': j.get('location', 'Remote'),
                        'description': j.get('description', ''),
                        'job_url': j.get('url', ''),
                        'date_posted': j.get('date', ''),
                        'site': 'RemoteOK',
                        'source_query': 'remoteok_api'
                    })
    except Exception as e:
        log_callback(f"Error fetching from RemoteOK: {e}")

    # 3. Fetch from Arbeitnow
    try:
        log_callback("Fetching from Arbeitnow API...")
        res = requests.get('https://www.arbeitnow.com/api/job-board-api', timeout=15)
        if res.ok:
            jobs_data = res.json().get('data', [])
            log_callback(f"    -> Arbeitnow returned {len(jobs_data)} total jobs.")
            for j in jobs_data:
                title = str(j.get('title', '')).lower()
                if is_relevant(title, search_terms):
                    all_jobs.append({
                        'job_title': j.get('title', ''),
                        'company': j.get('company_name', ''),
                        'location': j.get('location', 'Remote'),
                        'description': j.get('description', ''),
                        'job_url': j.get('url', ''),
                        'date_posted': j.get('created_at', ''),
                        'site': 'Arbeitnow',
                        'source_query': 'arbeitnow_api'
                    })
    except Exception as e:
        log_callback(f"Error fetching from Arbeitnow: {e}")

    # 4. Fetch from Himalayas
    try:
        log_callback("Fetching from Himalayas API...")
        res = requests.get('https://himalayas.app/jobs/api', timeout=15)
        if res.ok:
            jobs_data = res.json().get('jobs', [])
            log_callback(f"    -> Himalayas returned {len(jobs_data)} total jobs.")
            for j in jobs_data:
                title = str(j.get('title', '')).lower()
                if is_relevant(title, search_terms):
                    locs = j.get('locationRestrictions', [])
                    loc_str = ", ".join(locs) if isinstance(locs, list) else str(locs)
                    all_jobs.append({
                        'job_title': j.get('title', ''),
                        'company': j.get('companyName', ''),
                        'location': loc_str or 'Remote',
                        'description': j.get('description', ''),
                        'job_url': j.get('jobUrl', j.get('applicationLink', '')),
                        'date_posted': j.get('pubDate', ''),
                        'site': 'Himalayas',
                        'source_query': 'himalayas_api'
                    })
    except Exception as e:
        log_callback(f"Error fetching from Himalayas: {e}")

    # 5. Fetch from Jobicy
    try:
        log_callback("Fetching from Jobicy API...")
        res = requests.get('https://jobicy.com/api/v2/remote-jobs', timeout=15)
        if res.ok:
            jobs_data = res.json().get('jobs', [])
            log_callback(f"    -> Jobicy returned {len(jobs_data)} total jobs.")
            for j in jobs_data:
                title = str(j.get('jobTitle', '')).lower()
                if is_relevant(title, search_terms):
                    all_jobs.append({
                        'job_title': j.get('jobTitle', ''),
                        'company': j.get('companyName', ''),
                        'location': j.get('jobGeo', 'Remote'),
                        'description': j.get('jobDescription', ''),
                        'job_url': j.get('url', ''),
                        'date_posted': j.get('pubDate', ''),
                        'site': 'Jobicy',
                        'source_query': 'jobicy_api'
                    })
    except Exception as e:
        log_callback(f"Error fetching from Jobicy: {e}")

    # 6. Fetch from Findwork
    try:
        findwork_key = config.FINDWORK_API_KEY
        if findwork_key:
            log_callback("Fetching from Findwork API...")
            headers = {'Authorization': f'Token {findwork_key}'}
            query_term = search_terms[0] if search_terms else 'data analyst'
            res = requests.get(
                'https://findwork.dev/api/jobs/',
                params={'search': query_term},
                headers=headers,
                timeout=15,
            )
            if res.ok:
                jobs_data = res.json().get('results', [])
                log_callback(f"    -> Findwork returned {len(jobs_data)} total jobs.")
                for j in jobs_data:
                    title = str(j.get('role', '')).lower()
                    if is_relevant(title, search_terms):
                        all_jobs.append({
                            'job_title': j.get('role', ''),
                            'company': j.get('company_name', ''),
                            'location': j.get('location') or 'Remote',
                            'description': j.get('text', ''),
                            'job_url': j.get('url', ''),
                            'date_posted': j.get('date_posted', ''),
                            'site': 'Findwork',
                            'source_query': 'findwork_api'
                        })
    except Exception as e:
        log_callback(f"Error fetching from Findwork: {e}")

    # 7. Fetch from Jooble
    try:
        jooble_key = config.JOOBLE_API_KEY
        if jooble_key:
            log_callback("Fetching from Jooble API...")
            # We will just search the first term to keep it simple, or 'data analyst'
            query_term = search_terms[0] if search_terms else 'data analyst'
            jooble_url = f'https://jooble.org/api/{jooble_key}'
            res = requests.post(jooble_url, json={'keywords': query_term, 'location': 'remote'}, timeout=15)
            if res.ok:
                jobs_data = res.json().get('jobs', [])
                log_callback(f"    -> Jooble returned {len(jobs_data)} total jobs.")
                for j in jobs_data:
                    title = str(j.get('title', '')).lower()
                    if is_relevant(title, search_terms):
                        all_jobs.append({
                            'job_title': j.get('title', ''),
                            'company': j.get('company', ''),
                            'location': j.get('location', 'Remote'),
                            'description': j.get('snippet', ''),
                            'job_url': j.get('link', ''),
                            'date_posted': j.get('updated', ''),
                            'site': 'Jooble',
                            'source_query': 'jooble_api'
                        })
    except Exception as e:
        log_callback(f"Error fetching from Jooble: {e}")

    # 8. Fetch from Adzuna
    try:
        adzuna_app_id = config.ADZUNA_APP_ID
        adzuna_app_key = config.ADZUNA_APP_KEY
        if adzuna_app_id and adzuna_app_key:
            log_callback("Fetching from Adzuna API...")
            query_term = search_terms[0].replace(' ', '%20') if search_terms else 'data%20analyst'
            adzuna_url = f'https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={adzuna_app_id}&app_key={adzuna_app_key}&what={query_term}'
            res = requests.get(adzuna_url, timeout=15)
            if res.ok:
                jobs_data = res.json().get('results', [])
                log_callback(f"    -> Adzuna returned {len(jobs_data)} total jobs.")
                for j in jobs_data:
                    title = str(j.get('title', '')).lower()
                    if is_relevant(title, search_terms):
                        company_info = j.get('company', {})
                        location_info = j.get('location', {})
                        all_jobs.append({
                            'job_title': j.get('title', ''),
                            'company': company_info.get('display_name', ''),
                            'location': location_info.get('display_name', 'Remote'),
                            'description': j.get('description', ''),
                            'job_url': j.get('redirect_url', ''),
                            'date_posted': j.get('created', ''),
                            'site': 'Adzuna',
                            'source_query': 'adzuna_api'
                        })
            else:
                log_callback(f"    -> Adzuna Error: {res.status_code}")
    except Exception as e:
        log_callback(f"Error fetching from Adzuna: {e}")

    # 9. Fetch from USAJOBS
    try:
        usajobs_key = config.USAJOBS_API_KEY
        if usajobs_key:
            log_callback("Fetching from USAJOBS API...")
            query_term = search_terms[0].replace(' ', '+') if search_terms else 'data+analyst'
            usajobs_url = f'https://data.usajobs.gov/api/search?Keyword={query_term}'
            headers = {
                'Host': 'data.usajobs.gov',
                'User-Agent': 'jobscraper@example.com',
                'Authorization-Key': usajobs_key
            }
            res = requests.get(usajobs_url, headers=headers, timeout=15)
            if res.ok:
                data = res.json()
                jobs_data = data.get('SearchResult', {}).get('SearchResultItems', [])
                log_callback(f"    -> USAJOBS returned {len(jobs_data)} total jobs.")
                for item in jobs_data:
                    j = item.get('MatchedObjectDescriptor', {})
                    title = str(j.get('PositionTitle', '')).lower()
                    if is_relevant(title, search_terms):
                        all_jobs.append({
                            'job_title': j.get('PositionTitle', ''),
                            'company': j.get('OrganizationName', 'US Government'),
                            'location': j.get('PositionLocationDisplay', 'Remote'),
                            'description': j.get('QualificationSummary', ''),
                            'job_url': j.get('PositionURI', ''),
                            'date_posted': j.get('PublicationStartDate', ''),
                            'site': 'USAJOBS',
                            'source_query': 'usajobs_api'
                        })
            else:
                log_callback(f"    -> USAJOBS Error: {res.status_code}")
    except Exception as e:
        log_callback(f"Error fetching from USAJOBS: {e}")

    # 10. Fetch from The Muse
    try:
        themuse_key = config.THEMUSE_API_KEY
        if themuse_key:
            log_callback("Fetching from The Muse API...")
            # Using 'Data and Analytics' category since it maps perfectly to data analyst roles
            themuse_url = f'https://www.themuse.com/api/public/jobs?api_key={themuse_key}&category=Data%20and%20Analytics&page=1'
            res = requests.get(themuse_url, timeout=15)
            if res.ok:
                jobs_data = res.json().get('results', [])
                log_callback(f"    -> The Muse returned {len(jobs_data)} total jobs.")
                for j in jobs_data:
                    # Double check search terms, though category already heavily filters it
                    title = str(j.get('name', '')).lower()
                    if is_relevant(title, search_terms):
                        locations = j.get('locations', [])
                        loc_str = locations[0].get('name', 'Remote') if locations else 'Remote'
                        
                        all_jobs.append({
                            'job_title': j.get('name', ''),
                            'company': j.get('company', {}).get('name', ''),
                            'location': loc_str,
                            'description': j.get('contents', ''),
                            'job_url': j.get('refs', {}).get('landing_page', ''),
                            'date_posted': j.get('publication_date', ''),
                            'site': 'The Muse',
                            'source_query': 'themuse_api'
                        })
            else:
                log_callback(f"    -> The Muse Error: {res.status_code}")
    except Exception as e:
        log_callback(f"Error fetching from The Muse: {e}")

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        log_callback(f"Total Remote API Jobs after filtering: {len(df)}")
        return df
    else:
        log_callback("No Remote API jobs matched.")
        return pd.DataFrame()

if __name__ == "__main__":
    df = collect_remote_api_jobs(["analyst", "data", "product"])
    print(df.head())
    print(f"Total rows: {len(df)}")

import os
import pandas as pd
import config

def collect_manual_jobs():
    print("Checking for manually exported jobs...")
    
    if not os.path.exists(config.MANUAL_IMPORT_FILE):
        return pd.DataFrame()
        
    try:
        df = pd.read_csv(config.MANUAL_IMPORT_FILE)
        
        # Standardize column names if user used different ones
        # Example: map 'Job Title' to 'title'
        col_mapping = {
            'Job Title': 'title',
            'Company': 'company',
            'Location': 'location',
            'URL': 'job_url',
            'Link': 'job_url',
            'Description': 'description',
            'Date': 'date_posted'
        }
        df.rename(columns=lambda x: col_mapping.get(x, x.lower()), inplace=True)
        
        # Ensure minimum required columns exist
        for col in ['title', 'company', 'location', 'job_url', 'description', 'date_posted']:
            if col not in df.columns:
                df[col] = ''
                
        # Add source tracking
        df['source_query'] = 'manual_import'
        
        print(f"  -> Imported {len(df)} jobs from {config.MANUAL_IMPORT_FILE}.")
        
        return df
    except Exception as e:
        print(f"  -> Error reading manual import file: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = collect_manual_jobs()
    print(df.head())

import pandas as pd
import os

# Paths
DATA_DIR = 'data'
PROCESSED_DIR = 'processed_data'

if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

def process_housing():
    print("Processing Housing Data...")
    df = pd.read_csv(os.path.join(DATA_DIR, 'ZHVI.csv'))
    
    # Identify the date column (it's the first unnamed or named column usually)
    # Based on previous head, it looks like the first column is the date.
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    
    # Melt from wide to long
    df_long = df.melt(id_vars=['Date'], var_name='State', value_name='HomeValue')
    
    # Convert Date to datetime
    df_long['Date'] = pd.to_datetime(df_long['Date'])
    
    # Drop rows with missing values (if any)
    df_long = df_long.dropna()
    
    df_long.to_csv(os.path.join(PROCESSED_DIR, 'housing_processed.csv'), index=False)
    print(f"Saved housing_processed.csv with {len(df_long)} rows.")

def process_inflation():
    print("Processing Inflation Data...")
    
    # Load BLS data - note: BLS files use tabs
    # We use engine='python' and sep='\t' to be more robust
    df_data = pd.read_csv(os.path.join(DATA_DIR, 'cu.data.0.Current'), sep='\t')
    df_series = pd.read_csv(os.path.join(DATA_DIR, 'cu.series'), sep='\t')
    df_period = pd.read_csv(os.path.join(DATA_DIR, 'cu.period'), sep='\t')
    
    # Clean column names (strip whitespace)
    df_data.columns = [c.strip() for c in df_data.columns]
    df_series.columns = [c.strip() for c in df_series.columns]
    df_period.columns = [c.strip() for c in df_period.columns]
    
    # Clean cell values (strip whitespace)
    for df in [df_data, df_series, df_period]:
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].str.strip()

    # Filter for relevant series
    # CUSR0000SA0  : All items
    # CUSR0000SAH1 : Shelter
    # CUSR0000SA0E : Energy
    # CUSR0000SAF1 : Food
    relevant_ids = ['CUSR0000SA0', 'CUSR0000SAH1', 'CUSR0000SA0E', 'CUSR0000SAF1']
    df_data_filtered = df_data[df_data['series_id'].isin(relevant_ids)].copy()
    
    # Join with series metadata
    df_merged = df_data_filtered.merge(df_series[['series_id', 'series_title']], on='series_id', how='left')
    
    # Map months
    df_merged = df_merged.merge(df_period[['period', 'period_abbr']], on='period', how='left')
    
    # Create a proper Date column
    # period M01 -> 01
    df_merged['Month'] = df_merged['period'].str.replace('M', '').astype(int)
    # Ensure year is int
    df_merged['year'] = df_merged['year'].astype(int)
    
    # Construct date
    df_merged['Date'] = pd.to_datetime(df_merged['year'].astype(str) + '-' + df_merged['Month'].astype(str) + '-01')
    
    # Keep only necessary columns
    df_final = df_merged[['Date', 'series_title', 'value']].rename(columns={'value': 'CPI_Value', 'series_title': 'Metric'})
    
    df_final.to_csv(os.path.join(PROCESSED_DIR, 'inflation_processed.csv'), index=False)
    print(f"Saved inflation_processed.csv with {len(df_final)} rows.")

if __name__ == "__main__":
    process_housing()
    process_inflation()
    print("ETL Pipeline Complete!")

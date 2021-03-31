import pandas as pd
from datetime import datetime
import os

year = datetime.now().year - 1

def main():
  """A small program to download CDC Influenza test results for clinical and public health labs, and vaccine effectiveness tables.
  Reference:
    https://www.cdc.gov/flu/weekly/index.htm
    https://www.cdc.gov/flu/vaccines-work/past-seasons-estimates.html
  """
    folder_setup()
    clinical_labs()
    public_health_labs()
    vax_effectiveness()

def folder_setup():
    current_directory = os.getcwd()

    flu_data = os.path.join(current_directory, r'flu_data')
    
    vax_data = os.path.join(current_directory, r'vax_data')
    
    if not os.path.exists(flu_data):
       os.makedirs(flu_data)
    
    if not os.path.exists(vax_data):
       os.makedirs(vax_data)

def clinical_labs():
    for i in range(2015, year, 1):
        cl_urls = f'https://www.cdc.gov/flu/weekly/weeklyarchives{i}-{i+1}/data/whoAllregt_cl39.html'
        df_cl = pd.read_html(cl_urls)[0]
        df_cl.to_csv(f'flu_data/clinical_lab_{i}.csv', index=False)

def public_health_labs():
    for i in range(2015, year, 1):
        ph_urls = f'https://www.cdc.gov/flu/weekly/weeklyarchives{i}-{i+1}/data/whoAllregt_phl39.html'
        df_ph = pd.read_html(ph_urls)[0]
        df_ph.to_csv(f'flu_data/public_health_lab_{i}.csv', index=False)

def vax_effectiveness():
    for i in range(2011, year, 1):
        vax_url = f'https://www.cdc.gov/flu/vaccines-work/{i}-{i+1}.html'
        df = pd.read_html(vax_url)
        for table in range(0, len(df)):
            tables = df[table]
            tables.to_csv(f'vax_data/flu_vax_data{i}_table_{table}.csv', index=False)

if __name__=='__main__':
    main()

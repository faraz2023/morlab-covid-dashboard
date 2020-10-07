import requests, zipfile, io, os
import pandas as pd

def make_dir(path):
    try: os.mkdir(path)
    except:
      pass
make_dir('./data')
zip_file_url = 'https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip'
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./data/")

data = pd.read_csv("./data/13100781.csv", low_memory=False)
data = data[['Case identifier number','Case information','VALUE']]
data = data.pivot(index='Case identifier number', columns='Case information', values='VALUE')

data.sample(15000).to_csv('./data/Canadian_Covid_Cases_15000.csv')
data.to_csv('./data/Canadian_Covid_Cases.csv')

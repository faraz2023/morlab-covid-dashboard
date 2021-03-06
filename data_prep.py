import requests, zipfile, io, os
import pandas as pd
import datetime
def make_dir(path):
    try: os.mkdir(path)
    except:
      pass

data_path = "/var/www/html/flask/covidDash/covidDash"
make_dir(data_path + '/data')
zip_file_url = 'https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip'
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(data_path + "/data/")

data = pd.read_csv(data_path + "/data/13100781.csv", low_memory=False)
data = data[['Case identifier number','Case information','VALUE']]
data = data.pivot(index='Case identifier number', columns='Case information', values='VALUE')

data.sample(15000).to_csv(data_path + '/data/Canadian_Covid_Cases_15000.csv')
data.to_csv(data_path + '/data/Canadian_Covid_Cases.csv')

os.remove(data_path + "/data/13100781.csv")
os.remove(data_path + "/data/13100781_MetaData.csv")

print("Data Updated at {}".format(datetime.datetime.now()))

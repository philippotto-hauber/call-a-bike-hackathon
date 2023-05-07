import requests, zipfile, io

url = 'https://downloads.suche-postleitzahl.org/v2/public/plz-5stellig.shp.zip'
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(path = 'data/plz')




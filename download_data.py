import requests, zipfile, io

url_base = 'https://download-data.deutschebahn.com/static/datasets/callabike/20170516/'
file_names = [
                'OPENDATA_CATEGORY_CALL_A_BIKE',
                'OPENDATA_RENTAL_ZONE_CALL_A_BIKE',
                'OPENDATA_VEHICLE_CALL_A_BIKE',
                #'OPENDATA_BOOKING_CALL_A_BIKE' #commented out because data not available under the url
            ]
file_extension = '.zip'

for f in file_names:
    r = requests.get(url_base + f + file_extension)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path = 'data')

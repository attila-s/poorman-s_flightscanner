import requests

url = "https://be.wizzair.com/5.3.0/Api/asset/farechart"

payload = "{\"wdc\":false,\"flightList\":[{\"departureStation\":\"BUD\",\"arrivalStation\":\"NCE\",\"date\":\"2017-07-28\"},{\"departureStation\":\"NCE\",\"arrivalStation\":\"BUD\",\"date\":\"2017-07-25\"}],\"dayInterval\":3,\"adultCount\":1,\"childCount\":0,\"isRescueFare\":false}"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "dee3075d-cb32-cc80-eddb-c026cf60008d"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)




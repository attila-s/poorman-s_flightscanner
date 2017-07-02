import requests
import argparse
import datetime
import sys
import logging

# Parse args
parser = argparse.ArgumentParser('Poorman\'s flight scanner')
parser.add_argument('--from')
parser.add_argument('--to')
parser.add_argument('--start')
parser.add_argument('--end')

args = vars(parser.parse_args())
day=args['start']
till=args['end']

logging.debug(args)

# Determine time intervals and fetch flight
start_date = datetime.datetime.strptime(day, "%Y-%m-%d")
end_date = datetime.datetime.strptime(till, "%Y-%m-%d")

# validation
exit(1) if (end_date < start_date) else logging.info("Dates OK\n")


act_date =start_date
logging.info(start_date.date())
s = requests.Session()

def fetch(dep,dest,day,s):
  url = "https://be.wizzair.com/5.3.0/Api/asset/farechart"
  payload = "{\"wdc\":false,\"flightList\":[{\"departureStation\":\"" + dep + "\",\"arrivalStation\":\"" + dest + "\",\"date\":\"" + day + "\"},{\"departureStation\":\"" + dest + "\",\"arrivalStation\":\"" + dep + "\",\"date\":\"" + day + "\"}],\"dayInterval\":10,\"adultCount\":1,\"childCount\":0,\"isRescueFare\":false}"
  logging.debug(payload)
  headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
	'pragma': 'no-cache',
    'origin': 'https://wizzair.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'cache-control': 'no-cache',
    'authority': 'be.wizzair.com',
    'referer': 'https://wizzair.com/'
  }

  response = s.post(url, data=payload, headers=headers)

  print(response.text)



while (act_date < end_date):
  logging.debug(act_date.date())
  fetch(args['from'], args['to'], act_date.strftime("%Y-%m-%d"), s)
  act_date = act_date + datetime.timedelta(days=10)




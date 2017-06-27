import requests
import argparse
import datetime
import sys
import logging

# Parse args
parser = argparse.ArgumentParser('My program')
parser.add_argument('--dep')
parser.add_argument('--from')
parser.add_argument('--dest')
parser.add_argument('--till')

args = vars(parser.parse_args())
day=args['from']
till=args['till']

logging.debug(args)

# Determine time intervals and fetch flight
start_date = datetime.datetime.strptime(day, "%Y-%m-%d")
end_date = datetime.datetime.strptime(till, "%Y-%m-%d")

# validation
exit(1) if (end_date < start_date) else logging.info("Dates OK\n")


act_date =start_date
logging.info(start_date.date())

def fetch(dep,dest,day):
  url = "https://be.wizzair.com/5.3.0/Api/asset/farechart"
  payload = "{\"wdc\":false,\"flightList\":[{\"departureStation\":\"" + dep + "\",\"arrivalStation\":\"" + dest + "\",\"date\":\"" + day + "\"},{\"departureStation\":\"" + dest + "\",\"arrivalStation\":\"" + dep + "\",\"date\":\"" + day + "\"}],\"dayInterval\":10,\"adultCount\":1,\"childCount\":0,\"isRescueFare\":false}"
  logging.debug(payload)
  headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

  response = requests.request("POST", url, data=payload, headers=headers)

  print(response.text)



while (act_date < end_date):
  logging.debug(act_date.date())
  fetch(args['dep'], args['dest'], act_date.strftime("%Y-%m-%d"))
  act_date = act_date + datetime.timedelta(days=10)




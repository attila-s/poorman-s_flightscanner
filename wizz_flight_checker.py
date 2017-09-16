import requests
import argparse
import datetime
import sys
import logging
from requests_futures.sessions import FuturesSession
import json

# Ugly globals to pollute namespace

apiUrl = 'n/a'
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

aliases = {}

def parseArgs():
  parser = argparse.ArgumentParser('Poorman\'s flight scanner')
  parser.add_argument('--from')
  parser.add_argument('--to')
  parser.add_argument('--start')
  parser.add_argument('--end')
  parser.add_argument("-l", "--list", action="store_true", help="list destinations from departure")
  args = parser.parse_args()
  vargs = vars(args)
  day = vargs['start']
  till = vargs['end']

  logging.debug(vargs)

  start_date = datetime.datetime.now
  end_date = datetime.datetime.now
  if not args.list:
    # Determine time intervals and fetch flight
    start_date = datetime.datetime.strptime(day, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(till, "%Y-%m-%d")

    # validation
    exit(1) if (end_date < start_date) else logging.info("Dates OK\n")

    act_date = start_date
    logging.info(start_date.date())

  departure = vargs['from'].split(',')

  destinations=[]
  if not args.list:
    destinations = vargs['to'].split(',')
   
  action = 'scrape'
  if args.list:
    action = 'list'

  return (departure, destinations, start_date, end_date, action)

def fetch(dep, dest, day, s, futures):
  url = apiUrl +"/asset/farechart"
  payload = "{\"wdc\":false,\"flightList\":[{\"departureStation\":\"" + dep + "\",\"arrivalStation\":\"" + dest + "\",\"date\":\"" + day + "\"},{\"departureStation\":\"" + dest + "\",\"arrivalStation\":\"" + dep + "\",\"date\":\"" + day + "\"}],\"dayInterval\":10,\"adultCount\":1,\"childCount\":0,\"isRescueFare\":false}"
  logging.debug(payload)

  futures.append(s.post(url, data=payload, headers=headers))

def iterateDates(departure, destination, act_date, end_date, s, futures):
  while (act_date < end_date):
    logging.debug(act_date.date())
    fetch(departure, destination, act_date.strftime("%Y-%m-%d"), s, futures)
    act_date = act_date + datetime.timedelta(days=10)

def printFlights(futures):
  for response in futures:
    print(response.result().text)

def airlineEntryPoint():
  return "https://wizzair.com/static/metadata.json"

def getApiUrl(s):
  meta = s.get(airlineEntryPoint()).result().text
  jmeta = json.loads(meta)
  return jmeta['apiUrl']

def getFlightMap(s):
  url = apiUrl + '/asset/map'
  s.headers.update(headers)
  flightMap = s.get(url, params = {'languageCode' : 'en-gb'}).result().text

  return json.loads(flightMap)

def parseFlightMap(fmap):
  global aliases
  for c in fmap["cities"]:
    aliases[c["iata"]] = c["shortName"] + ", " + c["countryName"]
    
  return aliases

def isConnected(src, dst, fmap): 
  # Example: {"cities":[{"iata":"TIA","longitude":19.720555555555553,"latitude":41.414722222222224,"shortName":"Tirana","countryName":"Albania","countryCode":"AL","connections":[{"iata":"BUD","operationStartDate":"2017-07-05T00:00:00","rescueEndDate":"2017-07-03T06:47:28.6881332+01:00","isDomestic":false}],"aliases":["Tirana"],"isExcludedFromGeoLocation":false}
#
  cities = fmap["cities"]
  for c in cities:
    c_iata = c["iata"]
    if c_iata == src or c_iata == dst:
      connections = c["connections"]
      for conn in connections:
        conn_iata = conn["iata"]
        if conn_iata == src or conn_iata == dst:
          return True 
      return False
  return False

def listDestinations(src, fmap):
  print("Destinations from %s (%s): " % (src, aliases[src]))
  print("---")
  cities = fmap["cities"]
  conns = {}
  for c in cities:
    if c["iata"] == src:
      connections = c["connections"]
      for conn in connections:
         conns[conn["iata"]] = aliases[conn["iata"]]
  for key in sorted(conns):
    sys.stdout.write("%s: %s\n" % (key.encode('utf8'), conns[key].encode('utf8')))

def main():
  (departures, destinations, act_date, end_date, action) = parseArgs()

  s = FuturesSession()
  global apiUrl
  apiUrl = getApiUrl(s)
  logging.debug(getApiUrl(s))

  flightMap = getFlightMap(s)
  parseFlightMap(flightMap)

  if action == 'list':
    listDestinations(next(iter(departures)), flightMap)
    exit(0)

  futures = []
  for dep in departures:
    for dest in destinations:
      if isConnected(dep, dest, flightMap):
        iterateDates(dep, dest, act_date, end_date, s, futures)
      else:
	    sys.stderr.write("There is no connection between '%s' and '%s'!" % (departure, dest))
  printFlights(futures);

main()

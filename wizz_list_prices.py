#!/usr/bin/python
import sys
import json
import datetime
import argparse
import collections
import textwrap

parser = argparse.ArgumentParser(description='Display flight prices (downloaded from wizzair) in a convenient format.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\
Example:

python ~/wizz_list_prices.py -o Thursday Friday -r Monday Saturday Sunday --max 11000 BCN/BUD-BCN_201*'''))

parser.add_argument('prices', metavar='price_file',  nargs='+',
                    help='JSON file with prices from wizzair')
parser.add_argument('-m', '--max', help='max price  / ticket')
parser.add_argument('-o', '--out', help='outbound days', nargs='+')
parser.add_argument('-r', '--ret', help='return days', nargs='+')

args = parser.parse_args()
MAX = args.max
if MAX is None:
  MAX = sys.maxint
else:
  MAX = int(args.max)
print "Displaying flights whose price is <", MAX, "\n"

Flight = collections.namedtuple('Flight', ['out', 'ret', 'date', 'daz', 'price'], verbose=False) 
flight_map = []

def printFlights( flight_type ):
  for f in doc[flight_type]:      
    if f['price'] is None:
      continue
    price = int(float(f['price']['amount']))    
    if price > MAX:
      continue
    flight_date = f['date']
    
    weekday = datetime.datetime.strptime(flight_date, "%Y-%m-%dT%H:%M:%S").isoweekday()
    weekday = datetime.datetime.strptime(flight_date, "%Y-%m-%dT%H:%M:%S").strftime("%A")
    
    if flight_type == "outboundFlights" and not args.out is None and weekday not in args.out:
      continue
    if flight_type == "returnFlights" and not args.ret is None and weekday not in args.ret:
      continue
      
    ##if flight_type == "outboundFlights":
     ##sys.stdout.write(">> ")
    ##if flight_type == "returnFlights":
     ##sys.stdout.write("<< ") 
    
    flight = Flight(f['departureStation'], f['arrivalStation'], flight_date, weekday, f['price']['amount'])
    flight_map.append(flight)

for arg in args.prices:
  try:
    j=open(arg).read()
    doc=json.loads(j)
    printFlights('outboundFlights')
    printFlights('returnFlights')
  except:
    print arg, 'is strange'
    
for f in sorted(flight_map, key = lambda x : x[2]):
  print('%s %s %s %s\t%s' %f)

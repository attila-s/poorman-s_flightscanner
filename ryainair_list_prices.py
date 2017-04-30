import sys
import json
import datetime
import argparse
import collections
import textwrap

parser = argparse.ArgumentParser(description='Display flight prices (downloaded from ryanair) in a convenient format.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\
Example:

python ~/ryainair_list_prices.py -o Thursday Friday -r Monday Saturday Sunday --max 11000 BCN/BUD-BCN_201*'''))

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
sys.argv.pop(0)


Flight = collections.namedtuple('Flight', ['out', 'ret', 'date', 'daz', 'price'], verbose=False) 
flight_map = []

def printFlights():
  for t in doc["trips"]:  
    if t['destination'] is None:
      continue
    for d in t["dates"]:
      for f in d["flights"]:        
        price = f['regularFare']['fares'][0]['amount']      
        if price > MAX:
          continue
            
        flight_date = datetime.datetime.strptime(f["time"][0][:-4], "%Y-%m-%dT%H:%M:%S")
        weekday = flight_date.strftime("%A")
        
        print t['origin'], t['destination'], flight_date, weekday, str(price), doc["currency"]

for arg in args.prices:
  try:
    j=open(arg).read()
    doc=json.loads(j)  
    printFlights()
  except:
    print 'It is funny', arg

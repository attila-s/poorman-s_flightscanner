It is absolutely your sole responsibility to use these lines of code. No SLA or anything, you are on your own. If you plan to use any of this stuff, please be aware of licensing, which is default github :).

Hints:
##Create a Virtualenv
```
virtuelenv virt
source virt
```

##Install requirements
```
pip install -r devel-req.txt
```


```
$ python wizz_flight_checker.py --help
usage: Poorman's flight scanner [-h] [--from FROM] [--to TO] [--start START]
                                [--end END] [-l]

optional arguments:
  -h, --help     show this help message and exit
  --from FROM
  --to TO
  --start START
  --end END
  -l, --list     list destinations from departure
```

You migth want to take into account Wizzair's terms and conditions (you can be rejected to board if you are a bad citizen), so you might want to set up VPN. "Don't be evil."

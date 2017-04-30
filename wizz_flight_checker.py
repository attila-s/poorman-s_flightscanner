import requests

headers = {
    'origin': 'https://wizzair.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://wizzair.com/',
    'authority': 'be.wizzair.com',
    'cookie': '_ga=GA1.2.1420123030.1485595139; ASP.NET_SessionId=qllbmq1r2whhbxbz3cyp1gsm; _gat=1; ak_bmsc=4DC9B96B188DDBF1A6A463C5267D9725170671AC475B00002382C9587BFCDF12~plfIrbfClmwubqrCjT1Pa7wZ2Hpd7JOKhRkjSEbnaD5ulqvTHbq+SvTtlLnWMliz97KOhWlQJmI8Lu9EW8RsCuy2X3hvQ5lrPRHkgghQ71y5yiVOwpozy1w9CU7VN7cPnnfPDMLkqRccnHXeDNK7pSOtbBofi4Ascko5VsL0u24CFAogyVbhStcNhvQ9BFKfTFlkwG38adIUSgUxLHg9WH9Q==',
}

data = '{"wdc":false,"flightList":[{"departureStation":"BUD","arrivalStation":"MLA","date":"2017-03-24"}],"dayInterval":3,"adultCount":1,"childCount":0}'

requests.post('https://be.wizzair.com/4.1.0/Api/asset/farechart', headers=headers, data=data)

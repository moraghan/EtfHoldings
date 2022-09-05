import requests
import re
import pandas as pd

etf_keys = ['ARKK']
mutual_fund_keys = ['VFTAX']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
}


def main_etf(url):
    with requests.Session() as req:
        req.headers.update(headers)
        for key in etf_keys:
            r = req.get(url.format(key))
            print(f"Extracting: {r.url}")
            etf_stock_list = re.findall(r'etf\\\/(.*?)\\', r.text)
            print(etf_stock_list)
            etf_stock_details_list = re.findall(
                r'<\\\/span><\\\/span><\\\/a>",(.*?), "<a class=\\\"report_document newwin\\', r.text)
            df2 = pd.DataFrame(list(zip(etf_stock_list,etf_stock_details_list)),columns=['SYMBOL', 'VALUE'])
            for i,f in enumerate(df2['VALUE']):
                vals = f.lstrip().replace('"','').replace(',','').split(' ')
                qty = int(vals[0])
                weighting = vals[1]
                yeardiff = vals[2]

                print(etf_stock_list[i], qty, weighting, yeardiff)
            print(etf_stock_details_list)


def main_mutual(url):
    with requests.Session() as req:
        req.headers.update(headers)
        for key in mutual_fund_keys:
            r = req.get(url.format(key))
            print(f"Extracting: {r.url}")
            mutual_stock_list = re.findall(r'\\\/mutual-fund\\\/quote\\\/(.*?)\\', r.text)
            print(mutual_stock_list)
            mutual_stock_details_list = re.findall(r'"sr-only\\\"><\\\/span><\\\/span><\\\/a>",(.*?)%", "', r.text)
            print(mutual_stock_details_list)


main_etf("https://www.zacks.com/funds/etf/{}/holding")
#main_mutual("https://www.zacks.com/funds/mutual-fund/quote/{}/holding")

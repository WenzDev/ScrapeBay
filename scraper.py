# Surrender Monkeys Inc.
# 69/69/80085
# Written by The Ass Blaster 6900

from lxml import html
import requests
from pprint import pprint
import unicodecsv as csv
from traceback import format_exc
import argparse
import urllib3


def parse():
    # Disable warnings from urllib about Insecure Requests bcuz fuck that bullshit
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # from 12 to 14 I'm creating a search URL that will be input to LXML
    searchurl = "http://www.ebay.com/sch/"
    item = input("What are you looking into buying?")
    url = "".join([searchurl, item])
    print(url)
    for i in range(5):
        try:
            # You have to specify your browser headings or it'll break when it can't find a match
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/42.0.2311.90 Safari/537.36'}
            print("Fetching %s"%(url))
            # establishing what format your response will be in
            response = requests.get(url, headers=headers, verify=False)
            print("Scraping the Page" + " " + url)
            # declaring the parser text
            # http://saxon.sourceforge.net/saxon6.5.3/expressions.html
            # visit that link for more info on xpath or the expressions will seem foreign, surrender monkey
            parser = html.fromstring(response.text)
            p_list = parser.xpath('//li[contains(@class,"lvresult")]')
            # I could've used a metaclass here to define this whole area of parsing but I can't be arsed
            quant = parser.xpath("//span[@class='rcnt']//text()")
            # results = format quant.strip()
            results = ''.join(quant).strip()
            # Print found x results for {1} , {1} being the input variable from prompt
            print("Found {0} results for {1}".format(results, item))
            scraped_quant = []
            # I had to sign up on eBay's developer list to access their API variable names: "vip"
            # essentially href is an attribute of an html anchor tag (anchor tags identify sections of documents)
            # name with @class="vip" is their API variable for item name
            # price is self explanatory
            # the second declaration of them is for the CSV
            for products in p_list:
                raw_url = products.xpath('.//a[@class="vip"]/@href')
                raw_name = products.xpath('.//a[@class="vip"]/text()')
                raw_price = products.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()")
                price = ' '.join(' '.join(raw_price).split())
                title = ' '.join(' '.join(raw_name).split())
                data = {
                    'url': raw_url[0],
                    'title': title,
                    'price': price
                }
                scraped_quant.append(data)
                scraped_data = parse()
                print("Writing scraped data to %s-ebay-scraped-data.csv")

                with open('%s-ebay-scraped-data.csv', 'wb') as csvfile:
                    fieldnames = ["title", "price", "url"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    for data in scraped_data:
                        writer.writerow(data)
            return scraped_quant
        except Exception as e:
            print(format_exc(e))


if __name__ == '__main__':
    parse()





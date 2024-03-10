import sys
import csv
import requests
import datetime
import argparse

import wpdlutil
import WPcategories

import time
from bs4 import BeautifulSoup


######################
# argument setup
########################
parser = argparse.ArgumentParser()
parser.add_argument("-output", help="Output CSV file")
parser.add_argument("-categories", help="WordPress category slugs to include")
parser.add_argument("-exclude_categories", help="WordPress category slugs to EXCLUDE")
parser.add_argument ("-start_year", help="Starting year - get posts after this year")
parser.add_argument ("-start_month", help="Starting month - if start_year is set, get posts after this year and month")
parser.add_argument ("-domain", help="Domain of the WordPress site")
args = parser.parse_args()



headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    'Connection': "keep-alive",
    'Accept-Encoding': "gzip, deflate",
    'Postman-Token': "0,4eef3916-2e17-4176-81a5-1c5ade2848bc",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': args.domain,
    'cache-control': "no-cache"
    }

if args.start_year is None:
    start_year = 2012
else:
    start_year = args.start_year

if args.start_month is None:
    start_month = 1
else:
    start_month = args.start_month

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

print ("Getting posts from ", start_year,"-",start_month," to ", current_year, "-", current_month)

with open(args.output, "w+", encoding='utf-8', newline='') as destination:
    new_csv = csv.writer(destination)

    new_csv.writerow (['ID', 'Date', 'Slug', 'Title', 'Author', 'Categories', 'Author display','Post Content'])


    include_categories = exclude_categories = '0'
    if args.categories is not None:
        include_categories = WPcategories.get_category_ids (args.categories, True)
        print ("Getting categories: ", include_categories)
    if args.exclude_categories is not None:
        exclude_categories = WPcategories.get_category_ids (args.exclude_categories, True)
        print ("Excluding categories: ", exclude_categories)


    if (current_month < 12):
        next_month = str (current_year) + '-' + str (current_month + 1).rjust(2,'0')
    else:
        next_month = str (current_year + 1) + '-01'

    page = 1

    while page < 1000:
        print ('Getting page: ', page)

        url = 'https://' + args.domain + '/wp-json/wp/v2/posts/?categories=' + include_categories + '&categories_exclude=' + exclude_categories + '&after=' + str(start_year) + '-' + str(start_month).rjust(2,'0') + '-00T00:00:00&before=' + next_month + '-01T00:00:00&per_page=100&page=' + str(page)

        print (url)


        for attempt in range(5):
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                print ("successfully retrieved: ", url)
                break
            else:
                print ("error: ", resp.status_code)
                print (url)
                time.sleep(5)

        if resp.status_code != 200:
            print ("Final error: ", resp.status_code)
            print (url)
            break
        else:
            for post in resp.json():
                print ("Post: ", post['id'], '  --  ', post['title']['rendered'])
                #['ID', 'Date', 'Slug', 'Title', 'Author', 'Categories', 'Author display']

                if 'yoast_head_json' in post:
                    author = post['yoast_head_json']['author']
                else:
                    author = ''

                row = [post['id'], post['date'], post['slug'], wpdlutil.cleanhtml(post['title']['rendered']).encode('utf-8').decode('utf-8'), post['author'], post['categories'], author, post['content']['rendered']]
                new_csv.writerow (row)
                #])
            page += 1
            print("sleeping for 3")
            time.sleep(3)

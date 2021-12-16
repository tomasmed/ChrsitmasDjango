from django.db import connection
from bs4 import BeautifulSoup
import requests



# https://stackoverflow.com/questions/1074212/how-can-i-see-the-raw-sql-queries-django-is-running
def dump_queries() :
    qs = connection.queries
    for q in qs:
        print(q)

def get_link_info(url):
    req = requests.get(url)
    bs = BeautifulSoup(req.text, 'html.parser')

    webinfo = []

    title = bs.find(id="vi-lkhdr-itmTitl")
    webinfo.append(title)

    desc = bs.find(id="topItmCndDscMsg")
    webinfo.append(desc)

    price = bs.find(id="prcIsum")
    webinfo.append(price)

    return webinfo


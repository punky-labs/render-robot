import csv
import os, subprocess
import requests
import codecs
from contextlib import closing


def get_headers_local(path):
    try:
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            return list(dict(list(csv_reader)[0]).keys())
    except:
         return


def get_headers_remote(path):
    try:
        with closing(requests.get(path, stream=False)) as r:
                csv_reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
                return list(dict(list(csv_reader)[0]).keys())
    except:
         return

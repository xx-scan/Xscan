# coding=utf-8
import argparse
import ipaddress
import logging
import time

from .cli_output import start_out
from .common import start
from plugins.ActiveReconnaissance.active import ActiveCheck


def read_file(file, dbname):
    hosts = []
    try:
        with open(file, 'rt') as f:
            for ip in f.readlines():
                hosts.append(ip.strip())
        start_out(hosts)
        hosts2 = ActiveCheck(hosts).pool()
        for i in hosts2:
            start(i, dbname)
    except FileNotFoundError:
        print('input file')
    except Exception as e:
        logging.exception(e)


def inet(net, dbname):
    hosts = []
    try:
        result = list(ipaddress.ip_network(net).hosts())
        for ip in result:
            hosts.append(str(ip))
        start_out(hosts)
    except Exception as e:
        print("The task could not be carried out. {}".format(str(e)))
    hosts2 = ActiveCheck(hosts).pool()
    for i in hosts2:
        start(i, dbname)


def options():
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Vxscan V2.0')
    parser.add_argument("-u", "--url", help='Start scanning url -u xxx.com or -u url1,url2')
    parser.add_argument("-f", "--file", help='read the url from the file')
    parser.add_argument("-s", "--save", help='save in dbfile')
    parser.add_argument("-i", "--inet", help='cidr eg. 1.1.1.1 or 1.1.1.0/24')
    args = parser.parse_args()
    if args.save:
        dbname = args.save
    else:
        dbname = 'result'
    if args.inet:
        inet(args.inet, dbname)
    if args.url:
        start_out(args.url)
        if ActiveCheck([args.url]).pool():
            start(args.url, dbname)
    if args.file:
        read_file(args.file, dbname)
    end_time = time.time()
    if args.file or args.url or args.inet:
        # gener()
        print('\nrunning {0:.3f} seconds...'.format(end_time - start_time))
    else:
        print('No scan url, Please start scanning with -u or -f')

# coding=utf-8
import re

from virustotal_python import Virustotal

from lib.cli_output import console
from lib.iscdn import iscdn
from lib.settings import VIRUSTOTAL_API
from plugins.PassiveReconnaissance.ip_history import ipinfo


def virustotal(host):
    # VT接口，主要用来查询PDNS，绕过CDN
    pdns = []
    history_ip = []
    if VIRUSTOTAL_API:
        # noinspection PyBroadException
        try:
            vtotal = Virustotal(VIRUSTOTAL_API)
            if re.search(r'\d+\.\d+\.\d+\.\d+', host):
                return None
            resp = vtotal.domain_report(host)
            if resp.get('status_code') != 403:
                for i in resp.get('json_resp').get('resolutions'):
                    address = i.get('ip_address')
                    timeout = i.get('last_resolved')
                    if iscdn(address):
                        history_ip.append(address + ' : ' + timeout)
                pdns = history_ip[10:]
        except Exception:
            pass
    
    pdns.extend(ipinfo(host))
    
    if pdns:
        for i in pdns[:10]:
            console('PDNS', host, i + '\n')
    else:
        console('PDNS', host, 'None\n')
    return pdns

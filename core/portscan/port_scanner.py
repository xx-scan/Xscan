#!/usr/bin/env python3
# coding=utf-8

import nmap
import shortuuid
import requests
requests.packages.urllib3.disable_warnings()


# 调用 masscan
def portscan(scan_ip, opts=None, rate=2000):
    masscan_result_path = "masscan-result-{}.json".format(str(shortuuid.uuid()))
    masscan_shell = "{masscan_bin_path} {target} -p {port_list} {opts} -oJ {result_path} --rate {rate}".format(
        masscan_bin_path='/usr/local/bin/masscan',
        target=scan_ip,
        port_list="1-65535",
        result_path=masscan_result_path,
        rate=str(rate),
        opts=opts
    )
    return masscan_result_path



# 调用nmap识别服务
def Scan(scan_ip):
    nm = nmap.PortScanner()


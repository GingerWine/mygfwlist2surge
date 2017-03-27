#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

gfwlisturl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
g_config_file = "my_surge_conf.txt"
# server_ip = ""
# server_port = ""
# passwd = ""


def fetchGFWList(url=gfwlisturl):
    import urllib
    import base64
    response = urllib.urlopen(url)
    text_response = base64.decodestring(response.read())
    response.close()
    with open('translatedgfwlist.txt', 'w') as fout:
        fout.write(text_response)
    return text_response


def parse_translatedgfwlist(gfwlist=""):
    domains = set()
    gfwlist_lines = gfwlist.splitlines()
    for line in gfwlist_lines:
        if line.startswith("!"): # comments
            continue
        elif line.startswith("@@"): # white list
            continue
        elif line.startswith("["): # configuration
            continue
        elif line.find("*") > 0: # 通配符暂不处理
            continue

        elif line.startswith("||"): # domains
            line = line.lstrip("||")
        elif line.startswith("|"):
            line = line.lstrip("|")
        elif line.startswith("."):
            line = line.lstrip(".")

        domains.add(line)
        print line
    return domains

CONFIG = """
[General]
skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local
bypass-tun = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12
dns-server = 119.29.29.29, 223.5.5.5, 114.114.114.114
loglevel = notify

[Proxy]
Proxy = custom,%s,%s,aes-256-cfb,%s,http://surge.pm/ss.module

[Rule]
%s
IP-CIDR,91.108.4.0/22,Proxy,no-resolve
IP-CIDR,91.108.56.0/22,Proxy,no-resolve
IP-CIDR,109.239.140.0/24,Proxy,no-resolve
IP-CIDR,149.154.160.0/20,Proxy,no-resolve
IP-CIDR,10.0.0.0/8,DIRECT
IP-CIDR,127.0.0.0/8,DIRECT
IP-CIDR,172.16.0.0/12,DIRECT
IP-CIDR,192.168.0.0/16,DIRECT
GEOIP,CN,DIRECT
FINAL,DIRECT

"""

def generate_config(domains):
    proxy_name = "Proxy"
    rules = []
    for domain in domains:
        rule = "DOMAIN-SUFFIX,%s,%s,force-remote-dns" % (domain, proxy_name)
        rules.append(rule)

    rules_txt = "\n".join(rules)

    return CONFIG % (server_ip, server_port, passwd, rules_txt)


def process():
    gfwlist = fetchGFWList(gfwlisturl)
    print gfwlist
    domains = parse_translatedgfwlist(gfwlist)
    print domains
    config  = generate_config(domains)
    print config
    with open(g_config_file, 'w') as fout:
        fout.write(config)

def usage():
    print 'USAGE : '
    print 'python gfwlist2surge.py server_ip server_port password'

if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) != 4:
        usage()
        exit()
    print sys.argv
    global server_ip, server_port, passwd
    server_ip, server_port, passwd = sys.argv[1], sys.argv[2], sys.argv[3]
    process()



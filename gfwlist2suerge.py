#!/usr/bin/env python
# -*- coding: UTF-8 -*-

gfwlisturl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def fetchGFWList(url=gfwlisturl):
    import urllib
    import base64
    response = urllib.urlopen(url)
    text_response = base64.decodestring(response.read())
    response.close()
    with open('translatedgfwlist.txt', 'w') as fout:
        fout.write(text_response)


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
        elif line.find("*"): # 通配符暂不处理
            continue

        elif line.startswith("||"): # domains
            line = line.lstrip("||")
        elif line.startswith("|"):
            line = line.lstrip("|")





if __name__ == '__main__':
    fetchGFWList(gfwlisturl)


#!/usr/bin/python3

import base64
import hmac
import json
import re
import sys
import urllib.request
from urllib.parse import quote
from urllib import error
from _sha1 import sha1
import time
from datetime import datetime
import sys
import os
import ssl
import argparse

# author: TreviD
# date: 2020-02-21
# version: v0.2

aliddnsipv6_ak = "AccessKeyId"
aliddnsipv6_sk = "Access Key Secret"

# aliddnsipv6_ttl = "600"

params = {
    'Format': 'JSON',
    'Version': '2015-01-09',
    'AccessKeyId': aliddnsipv6_ak,
    'Signature': '',
    'SignatureMethod': 'HMAC-SHA1',
    'SignatureNonce': '',
    'SignatureVersion': '',
    'Timestamp': ''
}


def getSignature(params):
    list = []
    for key in params:
        # print(key)
        list.append(percentEncode(key) + "=" + percentEncode(str(params[key])))
    list.sort()
    CanonicalizedQueryString = '&'.join(list)
    # print("strlist:" + CanonicalizedQueryString)
    StringToSign = 'GET' + '&' + percentEncode("/") + "&" + percentEncode(CanonicalizedQueryString)
    # print("StringToSign:" + StringToSign)
    h = hmac.new(bytes(aliddnsipv6_sk + "&", encoding="utf8"),
                 bytes(StringToSign, encoding="utf8"), sha1)
    signature = base64.encodebytes(h.digest()).strip()
    signature = str(signature, encoding="utf8")
    # print(signature)
    return signature


def get_record_info(SubDomain, DomainName, Type):
    params = {
        'Format': 'JSON',
        'Version': '2015-01-09',
        'AccessKeyId': aliddnsipv6_ak,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': '',
        'SignatureVersion': '1.0',
        'Timestamp': '',
        'Action': 'DescribeSubDomainRecords'
    }
    params['DomainName'] = DomainName
    params['SubDomain'] = SubDomain + "." + DomainName
    params['Type'] = Type
    timestamp = time.time()
    formatTime = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - 8 * 60 * 60))
    params['Timestamp'] = formatTime
    params['SignatureNonce'] = timestamp

    Signature = getSignature(params)
    params['Signature'] = Signature
    list = []
    for key in params:
        list.append(percentEncode(key) + "=" + percentEncode(str(params[key])))
    list.sort()
    paramStr = "&".join(list)
    url = "https://alidns.aliyuncs.com/?" + paramStr
    # print("url:" + url)
    try:
        print("Looking up domain Info：" + SubDomain + " " + DomainName + " " + Type)
        context = ssl._create_unverified_context()
        jsonStr = urllib.request.urlopen(
            url, context=context).read().decode("utf8")
        print("Looking up finished,Result：" + jsonStr)
        return json.loads(jsonStr)
    except error.HTTPError as e:
        print(e)
        print("Looking up domain Info failed：" + e.read().decode("utf8"))


def add_domain_record(DomainName, RR, Type, Value):
    print("start add domain record")
    params = {
        'Format': 'JSON',
        'Version': '2015-01-09',
        'AccessKeyId': aliddnsipv6_ak,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': '',
        'SignatureVersion': '1.0',
        'Timestamp': '',
        'Action': 'AddDomainRecord'
    }
    params['DomainName'] = DomainName
    params['RR'] = RR
    params['Type'] = Type
    params['Value'] = Value

    timestamp = time.time()
    formatTime = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - 8 * 60 * 60))
    # formatTime = formatTime.replace(":", "%3A")
    params['Timestamp'] = formatTime
    params['SignatureNonce'] = timestamp

    Signature = getSignature(params)
    params['Signature'] = Signature
    list = []
    for key in params:
        list.append(percentEncode(key) + "=" + percentEncode(str(params[key])))
    list.sort()
    paramStr = "&".join(list)
    url = "https://alidns.aliyuncs.com/?" + paramStr
    # print("url:" + url)
    try:
        print("Registering " + RR + " " + DomainName + " " + Type + " " + Value)
        context = ssl._create_unverified_context()
        jsonStr = urllib.request.urlopen(
            url, context=context).read().decode("utf8")
        print("Registration Success")
        return json.loads(jsonStr)
    except error.HTTPError as e:
        print(e)
        print("Registration Failed：" + e.read().decode("utf8"))


def update_domain_record(RecordId, RR, Value, Type):
    print("start update domain record")
    params = {
        'Format': 'JSON',
        'Version': '2015-01-09',
        'AccessKeyId': aliddnsipv6_ak,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': '',
        'SignatureVersion': '1.0',
        'Timestamp': '',
        'Action': 'UpdateDomainRecord'
    }
    params['RecordId'] = RecordId
    params['RR'] = RR
    params['Type'] = Type
    params['Value'] = Value

    timestamp = time.time()
    formatTime = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.localtime(time.time() - 8 * 60 * 60))
    params['Timestamp'] = formatTime
    params['SignatureNonce'] = timestamp

    Signature = getSignature(params)
    params['Signature'] = Signature
    list = []
    for key in params:
        list.append(percentEncode(key) + "=" + percentEncode(str(params[key])))
    list.sort()
    paramStr = "&".join(list)
    url = "https://alidns.aliyuncs.com/?" + paramStr
    # print("url:" + url)
    try:
        print("Updating " + RR + " " + " " + Type + " " + Value)
        context = ssl._create_unverified_context()
        jsonStr = urllib.request.urlopen(
            url, context=context).read().decode("utf8")
        print("Update Success")
        return json.loads(jsonStr)
    except error.HTTPError as e:
        print(e)
        print("Update Failed：" + e.read().decode("utf8"))


def percentEncode(str):
    res = quote(str, 'utf8')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def get_Local_ipv6_address_win():
    """
        Get local ipv6
    """
    # pageURL = 'https://ip.zxinc.org/ipquery/'
    # pageURL = 'https://ip.sb/'
    pageURL = 'https://api-ipv6.ip.sb/ip'
    content = urllib.request.urlopen(pageURL).read()
    webContent = content.decode("utf8")

    print(webContent)
    ipv6_pattern = '(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'

    m = re.search(ipv6_pattern, webContent)

    if m is not None:
        return m.group()
    else:
        return None


def get_Local_ipv6_address_win2():
    """
        Get local ipv6
    """
    # pageURL = 'https://ip.zxinc.org/ipquery/'
    linelist = os.popen(''' ipconfig ''').readlines()
    webContent = ""
    for item in linelist:
        webContent += item

    print(linelist)
    ipv6_pattern = '(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'

    m = re.search(ipv6_pattern, webContent)

    if m is not None:
        return m.group()
    else:
        return None


def get_Local_ipv6_address_linux():
    """
        Get local ipv6
    """
    # pageURL = 'https://ip.zxinc.org/ipquery/'
    # pageURL = 'https://ip.sb/'
    linelist = os.popen(
        ''' ip -6 addr | grep "inet6.*global" | awk \'{print $2}\' | awk -F"/" \'{print $1}\' ''').readlines()  # 这个返回值是一个list
    if linelist:
        content = linelist[0].strip()
    else:
        return None
    ipv6_pattern = '(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'

    m = re.search(ipv6_pattern, content)

    if m is not None:
        return m.group()
    else:
        return None


def get_ipv4_net():
    context = ssl._create_unverified_context()
    res = urllib.request.urlopen("https://api.ip.sb/jsonip", context=context)
    return json.loads(res.read().decode('utf8'))['ip']


def get_local_ipv6():
    sysPlatform = sys.platform
    ipv6Addr = ""
    if sysPlatform == "linux":
        ipv6Addr = get_Local_ipv6_address_linux()
        print()
    elif sysPlatform == "win32":
        ipv6Addr = get_Local_ipv6_address_win2()
        # print()
    else:
        ipv6Addr = get_Local_ipv6_address_win()

    return ipv6Addr


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.description = 'Aliyun DDNS Tool'
    # parser.add_argument("key", help="从https://ak-console.aliyun.com/#/accesskey得到的AccessKeyId", type=str)
    # parser.add_argument("secret", help="从https://ak-console.aliyun.com/#/accesskey得到的AccessKeySecret", type=str)
    parser.add_argument("RR", help="RR Example：@, *, www, ...", type=str)
    parser.add_argument("DomainName", help="domain Example: aliyun.com, baidu.com, google.com, ...", type=str)
    parser.add_argument("Type", help="Type(A/AAAA)", type=str)
    parser.add_argument("--value", help="[value]", type=str)
    args = parser.parse_args()
    Type = ""
    ip = args.value
    if not ip:
        if args.Type.lower() == "a":
            ip = get_ipv4_net()
            Type = "A"
        elif args.Type.lower() == "aaaa":
            ip = get_local_ipv6()
            Type = "AAAA"
        else:
            print("Wrong Argument，Example：python3 ./aliddns.py www baidu.com A")
            exit()
    else:
        Type = args.Type.upper()

    RR = args.RR
    DomainName = args.DomainName

    print("Start Updating: RR:" + RR + " DomainName:" + DomainName)
    print("Local IP: " + ip)

    # client = AcsClient(args.key, args.secret, 'cn-hangzhou')
    recordListInfo = get_record_info(RR, DomainName, Type)

    if recordListInfo['TotalCount'] == 0:
        print("record not exists，register glue record")
        add_domain_record(DomainName, RR, Type, ip)
    else:
        records = recordListInfo["DomainRecords"]["Record"]
        hasFind = "false"
        for record in records:
            if record['RR'] == RR and record['DomainName'] == DomainName and record['Type'] == Type:
                hasFind = "true"
                if record['Value'] == ip:
                    print("no update needed")
                else:
                    print("update record")
                    update_domain_record(record['RecordId'], RR, ip, Type)
        if not hasFind:
            print("record not exists，register glue record")
            add_domain_record(DomainName, RR, Type, ip)

import smtplib
import configparser
import socket

'''
With this script you can check multiple SMTP accounts
Author: Mr128Bit
License: OpenSource
'''

alist = []
down_hosts = []
default_port = 587
settings = {}
config = configparser.RawConfigParser()


# Load all accounts into a list.
def get_accounts():
    with open('accounts.txt') as f:
        for line in f:
            alist.append(line)


# Iterate List to check all accounts in it.
def list_check():
    socket.setdefaulttimeout(7)
    print('Starting SMTP check of list...')
    for line in alist:
        split = line.split(':')
        host = 'smtp.' + split[0].split('@')[1]
        uname = split[0]
        pwd = split[1]
        single_check(host, uname, pwd)


# Check if host is reachable or not
def check_host(host, port):
    if host in down_hosts:
        return False
    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.close()
        return True
    except:
        down_hosts.append(host)
        return False


# Check Login of account
def single_check(smtphost, uname, pwd):
    port_conf = default_port if get_host_configuration(smtphost) is None else get_host_configuration(smtphost)

    if check_host(smtphost, port_conf):
        try:
            server = smtplib.SMTP(smtphost, port_conf)
            server.starttls()
            login = server.login(uname, pwd)[0]
            server.close()
        except:
            login = -1
        print('Login ' + ('un' if login != 235 else '') + 'successful! [' + uname + ']')
    else:
        print('[Warning] Can not connect to: ' + smtphost)


# Load Configuration file and set default port
def register_settings():
    config.read('smtp_settings.properties')
    default_port = int(config.get('DefaultSection', 'default.port'))


#Check if an advanced configuration for this host is available (smtp_settings.properties)
def get_host_configuration(host):
    a = host.split('.')
    a[len(host.split('.')) - 1] = '*'
    tmp = a
    h_host = '.'.join(a)
    try:
        port = config.get('AdvancedSection', h_host)
        return port
    except:
        return None


register_settings()
socket.setdefaulttimeout(7)
get_accounts()
list_check()

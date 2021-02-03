#!/usr/bin/env python3

from rocketchat.api import RocketChatAPI
from scapy.all import *
import time
import os

_AUTH_ = 'RWG'
# 3 January 2021 #

def Sniffer(interface,filter_parameter):
    #
    sniff(iface=interface,store=False,prn=ParsePacket,filter=filter_parameter)

def ParsePacket(pkt):
    #
    bot = RocketChatAPI(settings={
    'username':'wlan.bot',
    'password':'<password goes here>',
    'domain':'http://<Rocket Chat Server IP>:3000'
    })
    #
    if(pkt):
        #
        #pkt.show()
        #
        alert = ""
        #
        print("[*] DHCP Traffic Detected ")
        alert += " WLAN Association Detected \n"
        alert += " ------------------------------- \n"
        #
        source_addr = pkt['Ethernet'].src
        #
        raw_options = pkt['DHCP options'].options
        #
        time_stamp = time.ctime()
        #
        print("[*] Date/Time: %s " % time_stamp)
        alert += " Date/Time: %s \n" % time_stamp
        #
        host_name = raw_options[6][1]
        host_name = host_name.decode('utf-8')
        print("[*] Host name: %s " % host_name)
        alert+= " Host name: %s \n" % host_name
        #
        print("[*] Source MAC Address: %s " % source_addr)
        alert+= " Source MAC Address: %s \n" % source_addr
        #
        host_addr = raw_options[4][1]
        print("[*] Leased IP: %s " % host_addr)
        alert += " Leased IP: %s \n" % host_addr
        #
        try:
            #
            print("[*] Sending chat message...")
            #
            bot.send_message(alert,'homelab.coord')
            #
        except Exception as e:
            #
            print("[!] Failed to send notification: %s " % e)
            #
        time.sleep(1)
        #
        os.system('clear')
        #
        return

def main():
    #
    print("[*] Wireless LAN Monitor")
    #
    interface = 'eth0'
    #
    filter = "udp and (port 67 or 68)"
    #
    Sniffer(interface,filter)

if(__name__ == '__main__'):
    #
    main()

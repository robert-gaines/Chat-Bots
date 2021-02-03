#!/usr/bin/env python3

from rocketchat.api import RocketChatAPI
from ipstack import GeoLookup
from getpass import getpass
import subprocess
import smtplib
import time
import sys
import os
import re

sessions = list()

def GeolocateIP(ip):
    #
    geo_data = GeoLookup("<IP Stack API Key Goes Here>")
    #
    geo_location = geo_data.get_location(ip)
    #
    location_string = ""
    #
    location_string += "IP: "
    location_string += geo_location['ip']
    location_string += '\n'
    location_string += "City: "
    location_string += geo_location['city']
    location_string += '\n'
    location_string += "State: "
    location_string += geo_location['region_name']
    location_string += '\n'
    location_string += "Country: "
    location_string += geo_location['country_name']
    location_string += '\n'
    location_string += "Zip: "
    location_string += geo_location['zip']
    location_string += '\n'
    location_string += "Latitude: "
    location_string += str(geo_location['latitude'])
    location_string += '\n'
    location_string += "Longitude: "
    location_string += str(geo_location['longitude'])
    location_string += '\n'
    #
    return location_string

def MonitorNetwork(chat_instance):
	#
	while(True):
		#
		try:
			#
			raw = subprocess.check_output(['pivpn','-c'])
			#
			decoded = raw.decode('utf-8')
			#
			sock = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}"
			#
			username = "\w{1,100}.\.\w{1,100}\s"
			#
			if(len(sessions) >= 10):
				#
				sessions.clear()
				#
			if(re.search(sock,decoded)):
				#
				session = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}",decoded)
				#
				username = re.findall("\w{1,100}.\.\w{1,100}\s",decoded)
				#
				username = str(username[0])
				#
				session = str(session[0])
				#
				segments = session.split(':')
				#
				ip = segments[0] 
				#
				print("[*] Login Detected: %s - %s " % (username,session))
				#
				if(session not in sessions):
					#
					sessions.append(session)
					#
					print("[*] Sending notification ...")
					#
					try:
						#
						geo_ip_data = GeolocateIP(ip)
						#
					except:
						geo_ip_data = ""
						#
						continue
						#
					message_string = ""
					#
					message_string += "<-- VPN Login Notification --> \n"
					#
					message_string += time.ctime()
					#
					message_string += "\n"
					#
					message_string += "User: "
					#
					message_string += username
					#
					message_string += "\n"
					#
					message_string += "Socket: "
					#
					message_string += session
					#
					message_string += "\n"
					#
					message_string += geo_ip_data
					#
					room_id = "homelab.coord"
					#
					chat_instance.send_message(message_string,room_id)
					#
				else:
					#
					print("[~] Session is already present")
					#
			else:
				#
				print("[~] No session detected ...")
				#
			time.sleep(1)
			#
			os.system('clear')	
			#
			time.sleep(1)
			#
		except Exception as e:
			#
			print("[!] Exception: %s " % e)
			#
			pass
			#
		time.sleep(10)

def EstablishSession(username,password,server):
    #
    try:
        #
        chat_instance = RocketChatAPI(settings={
           'username':username,
           'password':password,
           'domain':server 
        })
        #
    except Exception as e:
        #
        print("[!] Error: %s " % e)
        #
        sys.exit(1)
        #
    return chat_instance

def main():
    #
    username = input("[+] Enter the Rocket Chat username->")
    #
    password = getpass("[+] Enter the Rocket Chat password-> ")
    #
    server   = input("[+] Enter the chat server URI-> ")
    #
    chat_session = EstablishSession(username,password,server)
    #
    while(True):
        #
        MonitorNetwork(chat_session)

if(__name__ == '__main__'):
    #
    main()


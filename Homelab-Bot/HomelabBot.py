from RocketChatBot import RocketChatBot
import subprocess
import requests
import socket
import time
import sys
import os

AllMentions = {}

class Bot:
    #
    def __init__(self,botname,botpass,server_url):
        #
        self.botname    = botname
        #
        self.botpass    = botpass
        #
        self.server_url = server_url
        #
        self.bot = RocketChatBot(self.botname,self.botpass,self.server_url)      
    
    def SendMessage(self,message,channel):
        #
        self.bot.send_message(message,channel_id=channel)

    def GenerateCat(self):
        #
        url = "https://api.thecatapi.com/v1/images/search?format=json"
        #
        payload = {}
        #
        headers = {
        'Content-Type': 'application/json',
        'x-api-key': '<CAT API KEY Goes here>'
        }
        #
        response = requests.request("GET", url, headers=headers, data = payload)
        #
        data = response.text.encode('utf8')
        #
        decode = data.decode('utf-8')
        #
        segments = decode.split(',')
        #
        url = segments[2].split(':')
        #
        url = url[2].split(':')
        #
        url = "https:"+url[0]
        #
        return url

    def HandleMention(self,message,channel):
        #
        if('hello' in message or 'hi' in message):
            #
            self.SendMessage('Greetings and salutations!',channel)
            #
        if('harambe' in message or 'Harambe' in message):
            #
            self.SendMessage('[R.I.P. Harambe](https://www.change.org/p/barack-obama-we-wish-for-there-to-be-a-harambe-memorial-outside-of-the-white-house)',channel)
            #
        if('kitten' in message or 'Kitten' in message):
            #
            self.SendMessage("[A random kitten, your excellency](http://www.randomkittengenerator.com/cats/rotator.php)",channel)
            #
        if('cat' in message or 'Cat' in message):
            #
            try:
                #
                url = self.GenerateCat()
                #
                cat_message = "[A random cat, your excellency](%s)" % url
                #
                self.SendMessage(cat_message,channel)
                #
            except:
                #
                self.SendMessage("There appears to be a sudden, unexplained cat deficiency",channel)
                #
        if('portscan' in message or 'PortScan' in message):
            #
            self.PortScan()
            #
        if('sweep' in message or 'Sweep' in message):
            #
            self.Sweep()
            #
        else:
            #
            return

    def CheckMentions(self):
        #
        headers = {
                    'X-Auth-Token':'<Token Goes Here>',
                    'X-User-Id':'<Bot User ID>'
                }
        #
        r = requests.get('http://<RC-Server IP Goes Here>:3000/api/v1/channels.getAllUserMentionsByChannel?roomId=BuC56sE9yDfB7kFr2',headers=headers)
        #
        if(r.status_code == 200):
            #
            content = r.json()
            #
            mentions = content['mentions']
            #
            for m in mentions:
                #
                message = m['msg']
                #
                timestamp = m['ts']
                #
                if(timestamp not in AllMentions):
                    #
                    self.HandleMention(message,'homelab.coord')
                    #
                    AllMentions[timestamp] = message

    def Sweep(self):
        #
        sweep_results = subprocess.check_output(['nmap','-sn','<SUBNET goes here>'])
        #
        sweep_results = sweep_results.decode('utf-8')
        #
        self.SendMessage(sweep_results,'homelab.coord')

    def PortScan(self):
        #
        scan_results = subprocess.check_output(['nmap','<SUBNET goes here>'])
        #
        scan_results = scan_results.decode('utf-8')
        #
        self.SendMessage(scan_results,'homelab.coord')

    def Handler(self):
        #
        self.SendMessage("Homelab Bot is here!",'homelab.coord')
        #
        while(True):
            #
            try:
                #
                self.CheckMentions()
                #
            except KeyboardInterrupt:
                #
                self.SendMessage("What do you expect me to do with that?",'homelab.coord')

if(__name__ == '__main__'):
    #
    b = Bot('homelab.bot','oqkwD7RQ6GQ0cqTbuDBH','http://<Rocket Chat Server IP>:3000')
    #
    b.Handler()

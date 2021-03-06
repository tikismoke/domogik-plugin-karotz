# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
===========

Send SMS on web service for french telephony providers : Orange, SFR, Bouygues, Freemobile.
Send Notification message with newtifry service.
Send Notification to karotz using tts.

Implements
========

- Class Karotz

@author: Nico <nico84dev@gmail.com>
@copyright: (C) 2007-2014 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import urllib, urllib2
import json
from domogik_packages.plugin_karotz.lib.client_devices import BaseClientService


class Karotz(BaseClientService):
    """ Karotz class
    """

    def update(self, params):
        """ Create or update internal data, must be overwrited.
            @param params :  domogik type.
                type : dict
            @param get_parameter : XplPlugin.get_parameter method.
                type : methode (device, key)
        """
        self.to = params['to']
        self.address = params['address'] if 'address' in params else None
        self.voice = params['voice']
        
    def request(self, url_to_send):
        print "http request : \n", url_to_send
        try:
            response = urllib2.urlopen(url_to_send)  # This request is sent in HTTP POST
        except IOError, e:
            print "failed : {0}".format(e)
            codeResult = e.code
            if codeResult == 400:
                error = 'A mandatory parameter is missing'  # Un des paramètres obligatoires est manquant.
            elif codeResult == 402:
                error = 'Too many SMS were sent in too little time.'  # Trop de SMS ont été envoyés en trop peu de temps.
            elif codeResult == 403:
                error = 'The service is not enabled on the subscriber area, or login / incorrect key.'  # Le service n’est pas activé sur l’espace abonné, ou login / clé incorrect.
            elif codeResult == 500:
                error = 'Server side error. Please try again later.'  # Erreur côté serveur. Veuillez réessayez ultérieurement.
            else:
                error = format(e)
            return {'status': 'TTS not sended', 'error': error}
        except urllib2.URLError, e:
            # For Python 2.6
            if isinstance(e.reason, socket.timeout):
                error = ("There was an error: %r" % e)
                return {'status': 'TTS not sended', 'error': error}
        except socket.timeout, e:  # For Python 2.7
            error = 'There was an error: %r" % e)'
            return {'status': 'TTS not sended', 'error': error}
        else:
            codeResult = response.getcode()
	    data = response.read()
            response.close()
            if codeResult == 200:
                error = ''  # Le SMS a été envoyé sur votre mobile.
                if 'msg' in data:
		    print data
		    #dumps the json object into an element
		    json_str = json.dumps(data)
		    print json_str
		    #load the json to a string
		    resp = json.loads(data)
		    print resp
		    error = resp['msg']
            elif codeResult == 400:
                error = 'A mandatory parameter is missing'  # Un des paramètres obligatoires est manquant.
            elif codeResult == 402:
                error = 'Too many SMS were sent in too little time.'  # Trop de SMS ont été envoyés en trop peu de temps.
            elif codeResult == 403:
                error = 'The service is not enabled on the subscriber area, or login / incorrect key.'  # Le service n’est pas activé sur l’espace abonné, ou login / clé incorrect.
            elif codeResult == 500:
                error = 'Server side error. Please try again later.'  # Erreur côté serveur. Veuillez réessayez ultérieurement.
	    else:
                error = 'Unknown error.'
        if error != '':
            return {'status': 'Not sended', 'error': error}
        else:
            return {'status': 'Sent', 'error': 'none'}

    def send_msg(self, body):
        print("send_msg : enter")
        data = urllib.urlencode({'text': "{0}".format(body)})
        url_sms = "http://" + self.address + "/cgi-bin/tts?" + self.voice + "&" + data
        result = self.request(url_sms)
        return result

    def action(self, actioncode):
        print("action : entrée")
        url_sms = "http://" + self.address + "/cgi-bin/" + actioncode
        result = self.request(url_sms)
        return result

    def earpos(self, position, ears):
        print("ear : entrée")
        url_sms = "http://" + self.address + "/cgi-bin/ears?" + ears + "=" + position + "&noreset=1"
        result = self.request(url_sms)
        return result

    def send(self, message):
        """ Send message
            @param message : message dict data contain at least keys:
                - 'to' : recipient of the message
                - 'header' : header for message
                - 'body" : message
                - extra key defined in 'command' json declaration like 'title', priority', ....
            @return : dict = {'status' : <Status info>, 'error' : <Error Message>}
        """
        print message
        msg = message['header'] + ': ' if message['header'] else ''
        if 'title' in message:
            msg = msg + ' ** ' + message['title'] + ' ** '
        if 'body' in message:
            msg = msg + message['body']
            result = self.send_msg(msg)
        elif 'sleep' in message:
            result = self.action("sleep")
        elif 'wakeup' in message:
            result = self.action("wakeup?silent=1")
        elif 'posleft' in message:
            result = self.earpos(message['posleft'], "right=0&left")
        elif 'posright' in message:
            result = self.earpos(message['posright'], "left=0&right")
        #elif 'colo' in message:
	#   resul = self.color()
	#/cgi-bin/leds?pulse=1&color=00FF00&speed=700&color2=000000
	else:
            result = "error"
        print result
        return result

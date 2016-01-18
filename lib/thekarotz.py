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
# from domogik_packages.plugin_karotz.lib.client_devices import BaseClientService
from client_devices import BaseClientService


class Karotz(BaseClientService):
    """ Notification Control karotz using tts
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
        
    def send_msg(self, body):
        print("send_msg : entrée")
        data = urllib.urlencode({'tts': "{0}".format(body)})
        url_sms = "http://" + self.address + "/cgi-bin/tts?voice=alice&nocache=0&voice=" + self.voice + "&text=" + data
        request = url_sms
        print "http request : \n", request
        try:
            response = urllib2.urlopen(request)  # This request is sent in HTTP POST
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
        else:
            codeResult = response.getcode()
            response.close()
            if codeResult == 200:
                error = ''  # Le SMS a été envoyé sur votre mobile.
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
            return {'status': 'TTS not sended', 'error': error}
        else:
            return {'status': 'TTS sended', 'error': ''}

    def action(self, actioncode):
        print("action : entrée")
        url_sms = "http://" + self.address + "/cgi-bin/" + actioncode
        request = url_sms
        print "http request : \n", request
        try:
            response = urllib2.urlopen(request)  # This request is sent in HTTP POST
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
            return {'status': 'Action error', 'error': error}
        else:
            codeResult = response.getcode()
            response.close()
            if codeResult == 200:
                error = ''  # Le SMS a été envoyé sur votre mobile.
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
            return {'status': 'Action error', 'error': error}
        else:
            return {'status': 'Action done', 'error': ''}

    def send(self, message):
        """ Send message
            @param message : message dict data contain at least keys:
                - 'to' : recipient of the message
                - 'header' : header for message
                - 'body" : message
                - extra key defined in 'command' json declaration like 'title', priority', ....
            @return : dict = {'status' : <Status info>, 'error' : <Error Message>}
        """
        msg = message['header'] + ': ' if message['header'] else ''
        if 'title' in message:
            msg = msg + ' ** ' + message['title'] + ' ** '
        if 'body' in message:
            msg = msg + message['body']
            result = self.send_msg(msg)
        elif 'sleep' in message:
            result = self.action("sleep")
        elif 'wakeup' in message:
            result = self.wakeup("wakeup?silent=1")
        else:
            result = "error"
        print result
        return result

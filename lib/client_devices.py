# !/usr/bin/python
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

Send SMS on web service for french telephony providers : Orange_sms-web, SFR_sms-web, Bouygues_sms-web, Freemobile_sms-web.

This is an upgrade based on sms plugin for domogik 0.3
@author: Gizmo - Guillaume MORLET <contact@gizmo-network.fr>

Implements
========

- class BaseClientService to handle Operators

@author: Nico <nico84dev@gmail.com>
@copyright: (C) 2007-2014 Domogik project
@license: GPL(v3)
@organization: Domogik
"""
OPERATORS_SERVICE = ['Karotz']


def createDevice(params, log=None):
    """ Create a device depending of operator, use instance for get parameters.
        - Developer : add your python class derived from DeviceBase class."""
    newOperator = None
    if params['operator'] == 'Karotz':
        from domogik_packages.plugin_karotz.lib.thekarotz import Karotz
        newOperator = Karotz(params, log)
    return newOperator


def GetDeviceParams(xplPlugin, device):
    """ Return all internal parameters depending of instance_type.
        - Developer : add your instance_type proper parameters
            @param xplPlugin : XplPlugin base class reference for "get_parameter" and "get_parameter_for_feature"" methods access.
                type : object class XplPlugin
            @param device :  domogik device data.
                type : dict
            @return : parameters for creating or update ClientService object.
                    Value must contain at least keys :
                        - 'operator' = Selected from OPERATORS_SERVICE
                        - 'to' = Client reference, the same as xPL key 'to'
                type : dict
    """
    print "Extract parameters from device : \n{0}".format(device)
    if device['device_type_id'] == 'karotz':
        operator = 'Karotz'
        id = xplPlugin.get_parameter_for_feature(device, 'xpl_stats', 'xPL_ack-msg', 'to')
        address = xplPlugin.get_parameter(device, 'address')
        voice = xplPlugin.get_parameter(device, 'voice')
        if operator and device["name"] and id and address and voice:
            params = {'name': device["name"], 'operator': operator, 'to': id, 'address': address, 'voice': voice}
            return params
    return None


class BaseClientService():
    """ Basic Class for operator functionnalities.
        - Developper : Use on inherite class to impllement new operator class
                Overwrite  methods to handle xpl event."""

    def __init__(self, params, log):
        """ Must be called and overwrited with operator parameters.
        """
        self._log = log
        self.update(params)
        if self._log: self._log.info(
            "Client {0} created , with parameters : {1}".format(self.__class__.__name__, params))

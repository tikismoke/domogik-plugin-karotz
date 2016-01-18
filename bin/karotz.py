#!/usr/bin/python
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
==============

Interact with karotz


Implements
========

- Karotz OpenKarotz API

@author: Tikismoke <new.domodroid@gmail.com>
@copyright: (C) 2013-2016 Domogik project
@license: GPL(v3)
@organization: Domogik
"""
# A debugging code checking import error
try:
    from domogik.xpl.common.xplconnector import Listener
    from domogik.xpl.common.xplmessage import XplMessage
    from domogik.xpl.common.plugin import XplPlugin

    from domogik_packages.plugin_karotz.lib.karotz import KarotzClientsManager
    from domogik_packages.plugin_karotz.lib.karotz_client import getClientId

    import traceback
except ImportError as exc:
    import logging

    logging.basicConfig(filename='/var/log/domogik/karotz_start_error.log', level=logging.DEBUG)
    log = logging.getLogger('KarotzManager_start_error')
    err = "Error: Plugin Starting failed to import module ({})".format(exc)
    print err
    logging.error(err)
    print log


class KarotzManager(XplPlugin):
    """ Envois et recois des codes xPL des notifications
    """

    def __init__(self):
        """ Init plugin
        """
        XplPlugin.__init__(self, name='karotz')

        # get the devices list
        self.devices = self.get_device_list(quit_if_no_device=False)
        # get the config values
        self.managerClients = KarotzClientsManager(self, self.send_xplTrig)
        for a_device in self.devices:
            try:
                if self.managerClients.addClient(a_device):
                    self.log.info("Ready to work with device {0}".format(getClientId(a_device)))
                else:
                    self.log.info("Device parameters not configured, can't create Karotz Client : {0}".format(
                        getClientId(a_device)))
            except:
                self.log.error(traceback.format_exc())
        # Create the xpl listeners
        Listener(self.handle_xpl_cmd, self.myxpl, {'schema': 'sendmsg.basic',
                                                   'xpltype': 'xpl-cmnd'})
        self.add_stop_cb(self.managerClients.stop)
        print "Plugin ready :)"
        self.log.info("Plugin ready :)")
        self.ready()

    def __del__(self):
        """Close managerClients"""
        print "Try __del__ self.managerClients."
        self.managerClients = None

    def send_xplStat(self, data):
        """ Send xPL Stat message on network
        """
        msg = XplMessage()
        msg.set_type("xpl-stat")
        msg.set_schema("sensor.basic")
        msg.add_data(data)
        self.myxpl.send(msg)

    def send_xplTrig(self, schema, data):
        """ Send xPL message on network
        """
        self.log.debug("Xpl Trig for {0}".format(data))
        msg = XplMessage()
        msg.set_type("xpl-trig")
        msg.set_schema(schema)
        msg.add_data(data)
        self.myxpl.send(msg)

    def send_xplCmd(self, data):
        """ Send xPL cmd message on network
        """
        print "send xpl-cmnd : {0}".format(data)
        msg = XplMessage()
        msg.set_type("xpl-cmnd")
        msg.set_schema("sendmsg.basic")
        msg.add_data(data)
        msg.set_source('domogik-dump_xpl.vmdomogik0')
        self.myxpl.send(msg)

    def handle_xpl_trig(self, message):
        self.log.debug("xpl-trig listener received message:{0}".format(message))
        print message

    def handle_xpl_cmd(self, message):
        """ Process xpl schema sendmsg.basic and
        """
        self.log.debug("xpl-cmds listener received message:{0}".format(message))
        device_name = message.data['to']
        self.log.debug("device :" + device_name)
        idsClient = self.managerClients.getIdsClient(device_name)
        find = False
        if idsClient != []:
            for id in idsClient:
                client = self.managerClients.getClient(id)
                if client:
                    self.log.debug("Handle xpl-cmds for Karotz client :{0}".format(message.data['to']))
                    find = True
                    client.handle_xpl_cmd(message.data)
        if not find: self.log.debug("xpl-cmds received for unknowns Karotz client :{0}".format(message.data['to']))


if __name__ == "__main__":
    KarotzManager()
